from collections import OrderedDict
import chess


from app.handlers import BaseHandler, engine


class GameHandler(BaseHandler):

    def get(self):
        fen = self.get_argument('fen', chess.STARTING_FEN)
        self.write_game(fen)

    def post(self):
        self.write_game(chess.STARTING_FEN)

    def write_game(self, fen:str):

        if self.get_argument('diagram', False):
            self.write_grid(fen)
            return

        board = chess.Board(fen)
        current_turn = board.turn
        output = OrderedDict([

            ('fen', fen),
            ('fullmove_number', board.fullmove_number),
            ('result', board.result()),
            ('is_game_over', board.is_game_over()),
            ('is_checkmate',board.is_checkmate()),
            ('is_stalemate', board.is_stalemate()),
            ('is_insufficient_material', board.is_insufficient_material()),
            ('is_seventyfive_moves', board.is_seventyfive_moves()),
            ('is_fivefold_repetition', board.is_fivefold_repetition()),

            ('white', OrderedDict([
                ('has_kingside_castling_rights', board.has_kingside_castling_rights(chess.WHITE)),
                ('has_queenside_castling_rights', board.has_queenside_castling_rights(chess.WHITE)),
            ])),

            ('black', OrderedDict([
                ('has_kingside_castling_rights', board.has_kingside_castling_rights(chess.BLACK)),
                ('has_queenside_castling_rights', board.has_queenside_castling_rights(chess.BLACK)),
            ])),

            ('turn', OrderedDict([
                ('color', 'white' if board.turn is chess.WHITE else 'black'),
                ('is_in_check', board.is_check()),
                ('legal_moves', [move.uci() for move in board.legal_moves]),
                ('can_claim_draw', board.can_claim_draw()),
                ('can_claim_fifty_moves', board.can_claim_fifty_moves()),
                ('can_claim_threefold_repetition', board.can_claim_threefold_repetition())
            ]))

        ])

        self.finish(output)

    def write_grid(self, fen:str):

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
