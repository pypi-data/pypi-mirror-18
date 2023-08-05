# Code to read HTTP data
#
# Strategy: each writer takes an event + a write-some-bytes function, which is
# calls.
#
# WRITERS is a dict describing how to pick a reader. It maps states to either:
# - a writer
# - or, for body writers, a dict of framin-dependent writer factories

import sys

from ._util import LocalProtocolError
from ._events import Data, EndOfMessage
from ._state import CLIENT, SERVER, IDLE, SEND_RESPONSE, SEND_BODY

__all__ = ["WRITERS"]

# Equivalent of bstr % values, that works on python 3.x for x < 5
if (3, 0) <= sys.version_info < (3, 5):
    def bytesmod(bstr, values):
        decoded_values = []
        for value in values:
            if isinstance(value, bytes):
                decoded_values.append(value.decode("ascii"))
            else:
                decoded_values.append(value)
        return (bstr.decode("ascii") % tuple(decoded_values)).encode("ascii")
else:
    def bytesmod(bstr, values):
        return bstr % values

def write_headers(headers, write):
    for name, value in headers:
        write(bytesmod(b"%s: %s\r\n", (name, value)))
    write(b"\r\n")

# XX FIXME: "Since the Host field-value is critical information for
# handling a request, a user agent SHOULD generate Host as the first
# header field following the request-line." - RFC 7230
def write_request(request, write):
    if request.http_version != b"1.1":
        raise LocalProtocolError("I only send HTTP/1.1")
    write(bytesmod(b"%s %s HTTP/1.1\r\n", (request.method, request.target)))
    write_headers(request.headers, write)

# Shared between InformationalResponse and Response
def write_any_response(response, write):
    if response.http_version != b"1.1":
        raise LocalProtocolError("I only send HTTP/1.1")
    status_bytes = str(response.status_code).encode("ascii")
    # We don't bother sending ascii status messages like "OK"; they're
    # optional and ignored by the protocol. (But the space after the numeric
    # status code is mandatory.)
    #
    # XX FIXME: could at least make an effort to pull out the status message
    # from stdlib's http.HTTPStatus table. Or maybe just steal their enums
    # (either by import or copy/paste). We already accept them as status codes
    # since they're of type IntEnum < int.
    write(bytesmod(b"HTTP/1.1 %s \r\n", (status_bytes,)))
    write_headers(response.headers, write)

class BodyWriter(object):
    def __call__(self, event, write):
        if type(event) is Data:
            self.send_data(event.data, write)
        elif type(event) is EndOfMessage:
            self.send_eom(event.headers, write)
        else:  # pragma: no cover
            assert False

#
# These are all careful not to do anything to 'data' except call len(data) and
# write(data). This allows us to transparently pass-through funny objects,
# like placeholder objects referring to files on disk that will be sent via
# sendfile(2).
#
class ContentLengthWriter(BodyWriter):
    def __init__(self, length):
        self._length = length

    def send_data(self, data, write):
        self._length -= len(data)
        if self._length < 0:
            raise LocalProtocolError(
                "Too much data for declared Content-Length")
        write(data)

    def send_eom(self, headers, write):
        if self._length != 0:
            raise LocalProtocolError(
                "Too little data for declared Content-Length")
        if headers:
            raise LocalProtocolError("Content-Length and trailers don't mix")

class ChunkedWriter(BodyWriter):
    def send_data(self, data, write):
        write(bytesmod(b"%x\r\n", (len(data),)))
        write(data)
        write(b"\r\n")

    def send_eom(self, headers, write):
        write(b"0\r\n")
        write_headers(headers, write)

class Http10Writer(BodyWriter):
    def send_data(self, data, write):
        write(data)

    def send_eom(self, headers, write):
        if headers:
            raise LocalProtocolError(
                "can't send trailers to HTTP/1.0 client")
        # no need to close the socket ourselves, that will be taken care of by
        # Connection: close machinery

WRITERS = {
    (CLIENT, IDLE): write_request,
    (SERVER, IDLE): write_any_response,
    (SERVER, SEND_RESPONSE): write_any_response,
    SEND_BODY: {
        "chunked": ChunkedWriter,
        "content-length": ContentLengthWriter,
        "http/1.0": Http10Writer,
    },
}
