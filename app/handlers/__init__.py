import os.path
from chess import uci

path = __path__[0] + '../../../engines/stockfish/Mac/stockfish-7-64'

engine = uci.popen_engine(os.path.abspath(path))
engine.uci()

from .base import BaseHandler
from .index import IndexHandler
from .game import GameHandler