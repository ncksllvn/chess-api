import os.path
import platform
from chess import uci

path = __path__[0]
system = platform.system()

if system == 'Darwin':
    path += '../../../engines/stockfish/Mac/stockfish-7-64'
else:
    raise Exception('No engine found for your OS.')

engine = uci.popen_engine(os.path.abspath(path))
engine.uci()

from .base import BaseHandler
from .index import IndexHandler
from .game import GameHandler