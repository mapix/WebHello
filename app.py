# -*- coding:utf-8 -*-


def application(environ, start_response):
    status = "200 OK"
    output = "Hello World!"
    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, application)
    print "Serving on port 8000..."
    httpd.serve_forever()
