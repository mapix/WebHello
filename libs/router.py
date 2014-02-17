
class Router(object):
    def __init__(self, config):
        self.config = config

    def __call__(self, environ):
        path_info = environ.get('PATH_INFO')
        if path_info in self.config:
            return self.config[path_info](environ)
        raise Exception("asdfads")

