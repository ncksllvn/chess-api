import tornado.web
from tornado.options import options

from app.handlers import IndexHandler, GameHandler


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/game', GameHandler),
        ]
        settings = dict(
            engine=options.path_to_engine,
            debug=options.debug,
        )
        super(Application, self).__init__(handlers, **settings)
