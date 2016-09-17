
import tornado.web
from tornado.options import define, options

from app.handlers import IndexHandler, GameHandler

define('port', default=5000, help='run on the given port', type=int)
define('debug', default=True, help='run in debug mode')


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/game', GameHandler),
        ]
        super(Application, self).__init__(handlers)