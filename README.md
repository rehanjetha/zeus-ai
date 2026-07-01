<p align="center">
  <img src="assets/zeus-ai-hero.svg" alt="Zeus AI banner" width="100%">
</p>

# Zeus AI

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Minimax](https://img.shields.io/badge/Search-Minimax-38BDF8?style=for-the-badge)
![Alpha Beta](https://img.shields.io/badge/Pruning-Alpha--Beta-FACC15?style=for-the-badge)
![Tests](https://github.com/rehanjetha/zeus-ai/actions/workflows/tests.yml/badge.svg)
![License](https://img.shields.io/badge/License-Source_Available--NC-A78BFA?style=for-the-badge)

Zeus AI is a Python checkers project built around a minimax-based player with
alpha-beta pruning. It was made to test a custom checkers move engine against a
simple random baseline and measure how well a deeper search strategy performs.

The project is intentionally small: `Player9.py` contains the Zeus move logic,
`PlayerRandom.py` provides a baseline opponent, and `CheckersSim.py` runs a
batch of simulated games between the two.

## At a Glance

| Area | What it does |
| --- | --- |
| Move generation | Finds legal movement, jumps, chained captures, and king movement |
| Search | Looks ahead with depth-limited minimax |
| Pruning | Uses alpha-beta pruning to skip branches that cannot improve the result |
| Heuristic | Scores boards using material, kings, promotion progress, center control, and edge control |
| Simulation | Runs repeated games against a random baseline player |

## Search Flow

<p align="center">
  <img src="assets/zeus-ai-search.svg" alt="Zeus AI minimax search flow" width="100%">
</p>

## Simulation Preview

<p align="center">
  <img src="assets/zeus-ai-board-snapshot.png" alt="Zeus AI board snapshot with a forced capture" width="80%">
</p>

## Project Structure

```text
zeus-ai/
├── CheckersSim.py   # Simulation runner
├── Player9.py       # Zeus AI player
└── PlayerRandom.py  # Random baseline player
```

## Running the Simulation

This project uses only the Python standard library.

Run the simulator with:

```bash
python CheckersSim.py
```

By default, `CheckersSim.py` runs 100 games between Zeus and the random player,
then prints the win and draw totals.

## Testing

Run the automated unit tests with:

```bash
python -m unittest discover -s tests
```

The tests cover forced captures, no-move handling, input-board immutability, and
deterministic behavior for the random baseline.

## How the AI Works

Zeus evaluates possible moves by searching ahead with minimax. On each turn, it
generates legal checkers moves, simulates future board states, scores each board,
and chooses the strongest move found at the configured search depth.

The board score rewards useful positions such as owned pieces, kings, pieces
closer to promotion, center control, and edge control. Opponent pieces and
strong opponent positions reduce the score.

## Notes

This is a compact project focused on checkers AI logic rather than a full
graphical game. The board is represented as nested Python lists, and pieces are
encoded as strings containing their color, position, and rank.

## License

This project is source-available for portfolio review and personal learning. It
is not licensed for commercial use, resale, redistribution, or incorporation
into another product without written permission.

See `LICENSE` for the full terms.
