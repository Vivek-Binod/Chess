A Python-based chess game with full implementation of standard chess rules

Built using the Pygame library for graphical interface and user interaction

Supports two-player mode (human vs human) and human vs AI mode

AI uses the Negamax algorithm with alpha-beta pruning for efficient move search

All major rules of chess are implemented:

	Castling

	En passant

	Pawn promotion (manual selection for human, automatic for AI)

	Check, checkmate, and stalemate detection

Smooth piece movement animations for a polished visual experience

Clean code structure split across main game logic, engine, and AI modules

To play as a human set either player one (white) or player true in chessmain.py to True, False implies AI will be playing the game/