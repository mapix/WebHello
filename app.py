# -*- coding:utf-8 -*-


from webhello.static import Static
from webhello.router import Router

from url import urls

application = Router(urls)
application = Static(application, ('/static/', 'static'),
                    {'/favicon.ico':'/static/favicon.ico'})

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, application)
    print "Serving on port 8000..."
    httpd.serve_forever()
