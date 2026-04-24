# Football Emulator

A console football tournament simulator with minute-by-minute match simulation, player stats, team analytics, and a full tournament bracket — all inside a terminal UI.

---

## Features

- **Tournament bracket** — 4 teams, round-by-round bracket view with results
- **Match simulation** — event-driven engine simulates all 90 minutes: goals, shots, fouls, corners, yellow/red cards
- **Physics-based probability** — goal chance derived from attacker rating, defender strength, and goalkeeper skill; minute intensity modifiers (pressure spikes at 31–45′ and 76–90′)
- **Home advantage** — home team gets a 1.15× power multiplier
- **Player selection** — attacker chosen by position priority (forward → winger → AM → CM) weighted by attack rating; defender weighted by defence rating
- **Team power** — calculated from squad average OVR × chemistry bonus × balance bonus (ideal 4-3-3 baseline) × synergy bonus
- **Player cards** — full stats per player: attack, defence, physical, technique, speed, stamina, mentality, OVR, potential, traits
- **Player comparison** — side-by-side stat comparison of any two players
- **Advanced stats** — possession %, shots / shots on target, fouls, corners, yellow cards per team; attack efficiency breakdown
- **ANSI colour output** — colour-coded menus, events, and player cards

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.x |
| Dependencies | stdlib only (`os`, `sys`, `time`, `random`, `json`, `math`) |
| Data | JSON flat files (`players.json`, `teams.json`, `matches.json`) |
| Architecture | MVC-like: `core/` (business logic) + `templates/` (rendering) + `source/` (entry point) |

---

## Quick Start

```bash
git clone https://github.com/Shipovmax/football_emulator
cd football_emulator
python source/main.py
```

No dependencies to install — stdlib only.

---

## Navigation

```
Main Menu
├── 1 — Tournament bracket  →  select match ID for details
│         └── Match details  →  simulate / lineups / detailed stats
├── 2 — Teams list          →  select team ID
│         └── Team card + roster  →  select player ID
│                   └── Player card  →  compare with another player
├── 3 — Players list        →  select player ID  →  player card
├── 4 — Simulate match      →  pick match from bracket
├── 5 — Advanced stats      →  top-5 OVR + per-team averages
└── 0 — Exit
```

---

## Project Structure

```
football_emulator/
├── assets/
│   ├── players.json       # 44 players with full attribute sets
│   ├── teams.json         # 4 teams (Dragons, Tigers, Eagles, Wolves)
│   └── matches.json       # Match schedule and results
├── core/
│   ├── data_loader.py     # JSON loading, chemistry calc, play style
│   ├── simulation.py      # MatchSimulator + LiveMatchSimulator
│   └── calculators.py     # PlayerCalculator, ChemistryCalculator, MatchCalculator, ProbabilityCalculator
├── templates/
│   ├── bracket.py         # Tournament bracket renderer
│   ├── match.py           # Match detail view + timeline
│   ├── players.py         # Player card, table, comparison
│   ├── teams.py           # Team card and table
│   ├── menu.py            # Main and secondary menus
│   ├── header.py          # App header
│   └── ended.py           # End screen
└── source/
    └── main.py            # Entry point + state machine (AdvancedFootballEmulator)
```

---

## Simulation Engine

Match events are generated minute by minute (1–90):

1. **Intensity check** — probability of any event occurring this minute (higher near half-time and full-time)
2. **Attack resolution** — home vs away based on relative team power; home advantage = 1.15×
3. **Goal probability** — `attacker.attack + technique` vs `defender.defence + goalkeeper.defence`; capped [0.05, 0.80]
4. **Event types** — goal (open play / header / long shot / penalty / free kick), shot on/off target, foul ± card, corner, offside
5. **Assist generation** — 70% of goals include a randomly selected assisting player

---

## Author

- GitHub: [Shipovmax](https://github.com/Shipovmax)
- Email: shipov.max@icloud.com
