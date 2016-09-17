from collections import OrderedDict
from tornado import gen
import chess

from app.handlers import BaseHandler, engine


class GameHandler(BaseHandler):

    def get(self):
        fen = self.get_argument('fen', None)
        self.write_board(fen)

    def post(self):
        self.write_board(board=chess.Board())

    @gen.coroutine
    def put(self):

        fen = self.get_argument('fen', None)
        move = self.get_argument('move', 'ai')

        if not fen:
            self.set_status(400)
            return

        if move == 'ai':
            yield self.do_ai_move(fen)
            return

        self.do_move(fen, move)

    @gen.coroutine
    def do_ai_move(self, fen):

        try:
            board = chess.Board(fen)

            yield engine.position(board, async_callback=True)
            command = engine.go(async_callback=True)

            yield command

            bestmove, ponder = command.result()

            board.push(bestmove)
            self.write_board(board=board)

        except ValueError:
            self.set_status(400)
            return

    def do_move(self, fen:str, move:str):

        try:
            board = chess.Board(fen)
            board.push_uci(move)
        except ValueError:
            self.set_status(400)
            return

        self.write_board(board=board)

    def write_board(self, fen:str='', board:chess.Board=None):

        if not board:
            try:
                board = chess.Board(fen)
            except ValueError:
                self.set_status(400)
                return

        if self.get_argument('format', 'json') == 'ascii':
            self.write_ascii(board.fen())
            return

        current_turn = board.turn
        output = OrderedDict([

            ('fen', board.fen()),
            ('fullmoveNumber', board.fullmove_number),
            ('result', board.result()),
            ('isGameOver', board.is_game_over()),
            ('isCheckmate',board.is_checkmate()),
            ('isStalemate', board.is_stalemate()),
            ('isInsufficientMaterial', board.is_insufficient_material()),
            ('isSeventyfiveMoves', board.is_seventyfive_moves()),
            ('isFivefoldRepetition', board.is_fivefold_repetition()),

            ('white', OrderedDict([
                ('hasKingsideCastlingRights', board.has_kingside_castling_rights(chess.WHITE)),
                ('hasQueensideCastlingRights', board.has_queenside_castling_rights(chess.WHITE)),
            ])),

            ('black', OrderedDict([
                ('hasKingsideCastlingRights', board.has_kingside_castling_rights(chess.BLACK)),
                ('hasQueensideCastlingRights', board.has_queenside_castling_rights(chess.BLACK)),
            ])),

            ('turn', OrderedDict([
                ('color', 'white' if board.turn is chess.WHITE else 'black'),
                ('isInCheck', board.is_check()),
                ('legalMoves', [move.uci() for move in board.legal_moves]),
                ('canClaimDraw', board.can_claim_draw()),
                ('canClaimFiftyMoves', board.can_claim_fifty_moves()),
                ('canClaimThreefoldRepetition', board.can_claim_threefold_repetition())
            ]))

        ])

        self.finish(output)

    def write_ascii(self, fen:str):

        """
        Loops through a game board and prints it out as ascii. Useful for debugging.
        For example, the starting board would print out:

        ---|--------------------------------
         8 | r | n | b | q | k | b | n | r |
        ---|--------------------------------
         7 | p | p | p | p | p | p | p | p |
        ---|--------------------------------
         6 |   |   |   |   |   |   |   |   |
        ---|--------------------------------
         5 |   |   |   |   |   |   |   |   |
        ---|--------------------------------
         4 |   |   |   |   |   |   |   |   |
        ---|--------------------------------
         3 |   |   |   |   |   |   |   |   |
        ---|--------------------------------
         2 | P | P | P | P | P | P | P | P |
        ---|--------------------------------
         1 | R | N | B | Q | K | B | N | R |
        ---|--------------------------------
           | a | b | c | d | e | f | g | h |

        """

        rows = fen.split(' ')[0].split('/')
        row_separator = '\n---|%s\n' % ('-' * 32)
        output = row_separator
        row_nums = reversed(range(1,9))

        for row_num, row in zip(row_nums, rows):
            output += ' %s | ' % row_num
            for piece in row:
                if piece.isdigit():
                    output += '  | ' * int(piece)
                else:
                    output += piece + ' | '
            output += row_separator

        output += '   | '
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            output += str(i) + ' | '

        self.finish(output)
