# Tiny Chess Engine

A compact alpha-beta chess engine in under 4,096 bytes of Python.

- 0x88 board, negamax with alpha-beta pruning
- Quiescence search (captures), transposition table
- MVV-LVA + killer move ordering
- Material + positional evaluation (centralisation, pawn push, bishop pair)
- Fixed node budget per move (deterministic, no clock)

Built for make.fun tiny-chess-01. MIT licensed.
