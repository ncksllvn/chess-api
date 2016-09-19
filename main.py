import os
import platform
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options


def setup():
    system = platform.system()
    engine_path = os.path.dirname(__file__)
    engine_paths = dict([
        ('Darwin', 'engines/stockfish/Mac/stockfish-7-64'),
        ('Darwin', 'engines/stockfish/Linux/stockfish-7-x64'),
    ])

    if not system in engine_paths:
        raise Exception('No engine for OS')

    engine_path = os.path.join(engine_path, engine_paths[system])

    define('port', default=5000, help='run on the given port', type=int)
    define('debug', default=True, help='run in debug mode')
    define('path-to-engine', default=engine_path, help='the location of the chess engine')

if __name__ == '__main__':
    setup()
    from app import Application
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
