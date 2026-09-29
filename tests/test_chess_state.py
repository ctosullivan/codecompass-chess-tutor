# tests.test_chess_state - tests for chess_tutor.chess_state.
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
"""Tests for the Phase 2A chess-state foundation.

Covers exactly what decisions/0010 and planning/ROADMAP.md's "Phase 2A
plan" ask for: FEN loading, legal-move handling, applying moves/state
transitions, and SAN/UCI round-tripping - nothing about concepts,
tablebases, or rendering, which are later phases.
"""

from __future__ import annotations

import pytest

from chess_tutor.chess_state import IllegalMoveError, Position

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# Verified empirically against python-chess directly before being used here
# (see planning/retros for the Phase 2A retro noting this practice) rather
# than assumed from memory of chess theory.
FOOLS_MATE_FEN = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
STALEMATE_FEN = "k7/8/KQ6/8/8/8/8/8 b - - 0 1"


class TestFenLoading:
    def test_starting_position_matches_python_chess_default(self) -> None:
        assert Position.starting().fen == STARTING_FEN

    def test_from_fen_round_trips(self) -> None:
        position = Position.from_fen(STARTING_FEN)
        assert position.fen == STARTING_FEN

    def test_from_fen_loads_arbitrary_position(self) -> None:
        position = Position.from_fen(STALEMATE_FEN)
        assert position.fen == STALEMATE_FEN
        assert position.white_to_move is False

    def test_from_fen_rejects_malformed_fen(self) -> None:
        with pytest.raises(ValueError):
            Position.from_fen("not a fen string")


class TestLegalMoves:
    def test_starting_position_has_twenty_legal_moves(self) -> None:
        # A standard, widely-known fact about the starting position: 16
        # pawn moves (8 pawns x 1-or-2 squares) + 4 knight moves (2 knights
        # x 2 squares) = 20. Asserted here as a sanity check on the wrapper,
        # not as a chess-theory claim this project is making independently.
        position = Position.starting()
        assert len(position.legal_moves_uci()) == 20
        assert len(position.legal_moves_san()) == 20

    def test_legal_moves_uci_contains_expected_opening_moves(self) -> None:
        position = Position.starting()
        moves = position.legal_moves_uci()
        assert "e2e4" in moves
        assert "g1f3" in moves

    def test_legal_moves_san_contains_expected_opening_moves(self) -> None:
        position = Position.starting()
        moves = position.legal_moves_san()
        assert "e4" in moves
        assert "Nf3" in moves

    def test_checkmate_position_has_no_legal_moves(self) -> None:
        position = Position.from_fen(FOOLS_MATE_FEN)
        assert position.legal_moves_uci() == []

    def test_stalemate_position_has_no_legal_moves(self) -> None:
        position = Position.from_fen(STALEMATE_FEN)
        assert position.legal_moves_uci() == []


class TestApplyingMoves:
    def test_apply_uci_returns_new_position_with_updated_fen(self) -> None:
        start = Position.starting()
        after = start.apply_uci("e2e4")
        assert after.fen != start.fen
        assert after.white_to_move is False

    def test_apply_san_returns_new_position_with_updated_fen(self) -> None:
        start = Position.starting()
        after = start.apply_san("e4")
        assert after.fen != start.fen
        assert after.white_to_move is False

    def test_apply_does_not_mutate_the_original_position(self) -> None:
        start = Position.starting()
        original_fen = start.fen
        start.apply_uci("e2e4")
        assert start.fen == original_fen

    def test_applying_a_full_game_reaches_fools_mate(self) -> None:
        position = Position.starting()
        for san in ["f3", "e5", "g4", "Qh4"]:
            position = position.apply_san(san)
        assert position.fen == FOOLS_MATE_FEN
        assert position.is_checkmate is True

    def test_apply_uci_rejects_illegal_move(self) -> None:
        start = Position.starting()
        with pytest.raises(IllegalMoveError):
            start.apply_uci("e2e5")

    def test_apply_san_rejects_illegal_move(self) -> None:
        start = Position.starting()
        with pytest.raises(IllegalMoveError):
            start.apply_san("Qh5")

    def test_apply_uci_rejects_malformed_move(self) -> None:
        start = Position.starting()
        with pytest.raises(IllegalMoveError):
            start.apply_uci("notamove")


class TestSanUciRoundTripping:
    def test_uci_move_and_san_move_reach_the_same_position(self) -> None:
        via_uci = Position.starting().apply_uci("e2e4")
        via_san = Position.starting().apply_san("e4")
        assert via_uci.fen == via_san.fen

    def test_applying_a_san_move_and_reading_it_back_as_uci(self) -> None:
        start = Position.starting()
        after_san = start.apply_san("Nf3")
        # Nf3 (SAN) is g1f3 (UCI) from the starting position - confirmed
        # empirically before writing this assertion.
        after_uci = start.apply_uci("g1f3")
        assert after_san.fen == after_uci.fen

    def test_a_move_present_in_uci_list_is_also_present_in_san_list(self) -> None:
        position = Position.starting()
        # e2e4 (UCI) and e4 (SAN) are the same move from the same position;
        # both listings should agree on how many legal moves there are.
        assert "e2e4" in position.legal_moves_uci()
        assert "e4" in position.legal_moves_san()
        assert len(position.legal_moves_uci()) == len(position.legal_moves_san())


class TestGameStateChecks:
    def test_starting_position_is_not_check_checkmate_or_stalemate(self) -> None:
        position = Position.starting()
        assert position.is_check is False
        assert position.is_checkmate is False
        assert position.is_stalemate is False
        assert position.is_game_over is False

    def test_fools_mate_is_checkmate_and_game_over_but_not_stalemate(self) -> None:
        position = Position.from_fen(FOOLS_MATE_FEN)
        assert position.is_checkmate is True
        assert position.is_stalemate is False
        assert position.is_game_over is True

    def test_stalemate_position_is_stalemate_and_game_over_but_not_checkmate(self) -> None:
        position = Position.from_fen(STALEMATE_FEN)
        assert position.is_stalemate is True
        assert position.is_checkmate is False
        assert position.is_game_over is True

    def test_check_without_mate_is_detected(self) -> None:
        # A black rook on e2 checks the white king on e1 along the e-file,
        # but the king has three legal escape squares - check, not mate.
        # Verified empirically before writing this assertion.
        position = Position.from_fen("4k3/8/8/8/8/8/4r3/4K3 w - - 0 1")
        assert position.is_check is True
        assert position.is_checkmate is False
        assert len(position.legal_moves_uci()) == 3
