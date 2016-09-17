import os.path
from chess import uci

path = __path__[0]

#engine = uci.popen_engine(os.path.abspath(path + '../../../stockfish/Mac/stockfish-7-64'))
#engine.uci()

from .base import BaseHandler
from .index import IndexHandler
from .game import GameHandler