import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options

from app import Application

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
