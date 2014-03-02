# -*- coding:utf-8 -*-

from cgi import escape
from .response import Response

"""
http://www.w3schools.com/tags/ref_httpmessages.asp

1xx: Information Message:
    Description:
        100 Continue     The server has received the request headers, and the client should proceed to send the request body
        101 Switching Protocols The requester has asked the server to switch protocols
        103 Checkpoint  Used in the resumable requests proposal to resume aborted PUT or POST requests

2xx: Successful Message:
    Description:
        200 OK  The request is OK (this is the standard response for successful HTTP requests)
        201 Created The request has been fulfilled, and a new resource is created
        202 Accepted    The request has been accepted for processing, but the processing has not been completed
        203 Non-Authoritative Information   The request has been successfully processed, but is returning information that may be from another source
        204 No Content  The request has been successfully processed, but is not returning any content
        205 Reset Content   The request has been successfully processed, but is not returning any content, and requires that the requester reset the document view
        206 Partial Content The server is delivering only part of the resource due to a range header sent by the client

3xx: Redirection Message:
    Description:
        300 Multiple Choices    A link list. The user can select a link and go to that location. Maximum five addresses
        301 Moved Permanently   The requested page has moved to a new URL
        302 Found   The requested page has moved temporarily to a new URL
        303 See Other   The requested page can be found under a different URL
        304 Not Modified    Indicates the requested page has not been modified since last requested
        306 Switch Proxy    No longer used
        307 Temporary Redirect  The requested page has moved temporarily to a new URL
        308 Resume Incomplete   Used in the resumable requests proposal to resume aborted PUT or POST requests

4xx: Client Error Message:
    Description:
        400 Bad Request The request cannot be fulfilled due to bad syntax
        401 Unauthorized    The request was a legal request, but the server is refusing to respond to it. For use when authentication is possible but has failed or not yet been provided
        402 Payment Required    Reserved for future use
        403 Forbidden   The request was a legal request, but the server is refusing to respond to it
        404 Not Found   The requested page could not be found but may be available again in the future
        405 Method Not Allowed  A request was made of a page using a request method not supported by that page
        406 Not Acceptable  The server can only generate a response that is not accepted by the client
        407 Proxy Authentication Required   The client must first authenticate itself with the proxy
        408 Request Timeout The server timed out waiting for the request
        409 Conflict    The request could not be completed because of a conflict in the request
        410 Gone    The requested page is no longer available
        411 Length Required The "Content-Length" is not defined. The server will not accept the request without it
        412 Precondition Failed The precondition given in the request evaluated to false by the server
        413 Request Entity Too Large    The server will not accept the request, because the request entity is too large
        414 Request-URI Too Long    The server will not accept the request, because the URL is too long. Occurs when you convert a POST request to a GET request with a long query information
        415 Unsupported Media Type  The server will not accept the request, because the media type is not supported
        416 Requested Range Not Satisfiable The client has asked for a portion of the file, but the server cannot supply that portion
        417 Expectation Failed  The server cannot meet the requirements of the Expect request-header field

5xx: Server Error Message:
    Description:
        500 Internal Server Error   A generic error message, given when no more specific message is suitable
        501 Not Implemented The server either does not recognize the request method, or it lacks the ability to fulfill the request
        502 Bad Gateway The server was acting as a gateway or proxy and received an invalid response from the upstream server
        503 Service Unavailable The server is currently unavailable (overloaded or down)
        504 Gateway Timeout The server was acting as a gateway or proxy and did not receive a timely response from the upstream server
        505 HTTP Version Not Supported  The server does not support the HTTP protocol version used in the request
        511 Network Authentication Required The client needs to authenticate to gain network access
"""

class HTTPException(Response, Exception):

    @property
    def html(self):
        return "An error has occurred"


class HTTPRedirection(HTTPException):
    status = "300 Multiple Choices"
    explanation = ("A link list. The user can select a link and go to that location."
                   " Maximum five addresses")

    def __init__(self, location, output="", request=None):
        super(HTTPRedirection, self).__init__(output, request)
        self.location = location
        self.response_headers.append(("Location", location))

    @property
    def html(self):
        localtion = escape(self.location)
        return """%s, you can visit new url with link: <a href="%s">%s</a>""" % (
                self.explanation, location, location)


class HTTPMovedPermanently(HTTPRedirection):

    status = "301 Moved Permanently"
    explanation = "The requested page has moved to a new URL"


class HTTPFound(HTTPRedirection):

    status = "302 Found"
    explanation = "The requested page has moved temporarily to a new URL"


class HTTPClientError(HTTPException):

    status = "400 Bad"
    explanation = "Request The request cannot be fulfilled due to bad syntax"

    @property
    def html(self):
        url = escape(self.request.get_url())
        return """%s, original request url:<a href="%s">%s</a>""" % (self.explanation, url, url)



class HTTPForbidden(HTTPClientError):

    status = "403 Forbidden"
    explanation = "The request was a legal request, but the server is refusing to respond to it"


class HTTPNotFound(HTTPClientError):

    status = "404 Not Found"
    explanation = "The requested page could not be found but may be available again in the future"


class HTTPServerError(HTTPException):

    status = "500 Internal Server Error"
    explanation = "A generic error message, given when no more specific message is suitable"
