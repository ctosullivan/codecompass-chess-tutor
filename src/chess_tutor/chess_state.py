# chess_tutor.chess_state - the chess-state primitive, wrapping python-chess.
# Copyright (C) 2026  Cormac O'Sullivan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Chess-state primitive for the tutor.

python-chess (GPL-3.0-or-later) is used directly as a normal runtime
dependency - see decisions/0010-gpl-relicensing-and-dependency-simplification.md.
This module exists to keep the rest of the domain depending on one small,
testable interface for chess-state operations, rather than importing
`chess` directly everywhere - an ordinary separation-of-concerns boundary,
not a licensing isolation boundary (decisions/0010 explicitly retires that
reasoning).

Scope: this module owns FEN loading, legal-move enumeration, applying a
move (by UCI or SAN) to produce a new position, and basic game-state
checks (check/checkmate/stalemate). It does not know about tablebases,
concepts, learners, or rendering - those are later roadmap items with
their own modules.
"""

from __future__ import annotations

from dataclasses import dataclass

import chess


class IllegalMoveError(ValueError):
    """Raised when a move cannot be applied to a position.

    Wraps whatever python-chess itself raised (its exception types -
    ``chess.IllegalMoveError``, ``chess.InvalidMoveError``,
    ``chess.AmbiguousMoveError``, all ``ValueError`` subclasses - are not
    exposed outside this module, per the module boundary above).
    """

    def __init__(self, move: str, fen: str) -> None:
        self.move = move
        self.fen = fen
        super().__init__(f"illegal move {move!r} in position {fen!r}")


@dataclass(frozen=True)
class Position:
    """An immutable chess position.

    Wraps a `chess.Board`. Methods that would change state (applying a
    move) return a *new* `Position` rather than mutating this one - the
    underlying python-chess board is always copied first, so a `Position`
    a caller is holding never changes under it.
    """

    board: chess.Board

    @classmethod
    def from_fen(cls, fen: str) -> "Position":
        """Load a position from Forsyth-Edwards Notation."""
        return cls(board=chess.Board(fen))

    @classmethod
    def starting(cls) -> "Position":
        """The standard chess starting position."""
        return cls(board=chess.Board())

    @property
    def fen(self) -> str:
        """This position's FEN, as produced by python-chess."""
        return self.board.fen()

    @property
    def white_to_move(self) -> bool:
        return self.board.turn == chess.WHITE

    def legal_moves_uci(self) -> list[str]:
        """Every legal move from this position, in UCI notation."""
        return [move.uci() for move in self.board.legal_moves]

    def legal_moves_san(self) -> list[str]:
        """Every legal move from this position, in Standard Algebraic Notation."""
        return [self.board.san(move) for move in self.board.legal_moves]

    def apply_uci(self, move_uci: str) -> "Position":
        """Apply a move given in UCI notation, returning the resulting position."""
        new_board = self.board.copy()
        try:
            new_board.push_uci(move_uci)
        except ValueError as exc:
            # Covers chess.IllegalMoveError, chess.InvalidMoveError, and
            # chess.AmbiguousMoveError - all direct ValueError subclasses
            # with no shared common ancestor other than ValueError itself.
            raise IllegalMoveError(move=move_uci, fen=self.fen) from exc
        return Position(board=new_board)

    def apply_san(self, move_san: str) -> "Position":
        """Apply a move given in Standard Algebraic Notation, returning the resulting position."""
        new_board = self.board.copy()
        try:
            new_board.push_san(move_san)
        except ValueError as exc:
            raise IllegalMoveError(move=move_san, fen=self.fen) from exc
        return Position(board=new_board)

    @property
    def is_checkmate(self) -> bool:
        return self.board.is_checkmate()

    @property
    def is_stalemate(self) -> bool:
        return self.board.is_stalemate()

    @property
    def is_check(self) -> bool:
        return self.board.is_check()

    @property
    def is_game_over(self) -> bool:
        return self.board.is_game_over()
