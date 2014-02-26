# -*- coding:utf-8 -*-


from webhello.static import Static

from libs.template import serve_template
from libs.router import Router


def index(environ):
    return """<form action='/hello'>
                <label>Name:</label>
                <input type='text' name='name'>
                <input type='submit' name='submit'>
              </form>"""

def hello(environ):
    query = environ['QUERY_STRING']
    print query
    params = dict(p.split('=') for p in query.split('&'))
    name = params.get('name', 'world')
    return serve_template('hello.html', **locals())


def application(environ, start_response):
    status = "200 OK"

    router = Router({'/':index, '/hello': hello})
    output = router(environ)

    output += "<table style='background-color:red;margin-top:100px'>"
    for k, v in environ.items():
        output += "<tr><td>%s=%s</td></tr>" % (k, v)
    output += "</table>"

    response_headers = [('Content-Type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    application = Static(application, ('/static/', 'static'), {'/favicon.ico':'/static/favicon.ico'})
    httpd = make_server('', 8000, application)
    print "Serving on port 8000..."
    httpd.serve_forever()
