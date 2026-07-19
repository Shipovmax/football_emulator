from typing import Any, Dict, List

GREEN_COLOR = "\033[92m"
BLUE_COLOR = "\033[94m"
YELLOW_COLOR = "\033[93m"
RED_COLOR = "\033[91m"
PURPLE_COLOR = "\033[95m"
CYAN_COLOR = "\033[96m"
RESET_COLOR = "\033[0m"


def print_player_card_ascii(player: Dict[str, Any]) -> None:
    position_translation = {
        "goalkeeper": "Goalkeeper",
        "center_back": "Center Back",
        "fullback": "Fullback",
        "defensive_midfielder": "Def. Mid",
        "center_midfielder": "Center Mid",
        "attacking_midfielder": "Att. Mid",
        "winger": "Winger",
        "forward": "Forward",
    }

    position = position_translation.get(player["position"], player["position"])
    overall = player["overall"]

    if overall >= 85:
        border_color = PURPLE_COLOR
    elif overall >= 75:
        border_color = YELLOW_COLOR
    else:
        border_color = GREEN_COLOR

    name = player["name"][:18].center(18)
    position_display = position.center(18)

    card = [
        f"{border_color}╔══════════════════════╗{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR}      {name}      {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR}    {position_display}    {border_color}║{RESET_COLOR}",
        f"{border_color}╠══════════════════════╣{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Attack:  {player['attack']:3d}       {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Defence: {player['defence']:3d}       {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Physical:{player['physical']:3d}       {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Technique:{player['technique']:3d}      {border_color}║{RESET_COLOR}",
        f"{border_color}╚══════════════════════╝{RESET_COLOR}",
    ]

    for line in card:
        print(line)


def print_player_card_detailed(player: Dict[str, Any]) -> None:
    border_color = BLUE_COLOR
    value_color = YELLOW_COLOR

    name = player["name"][:20].center(20)
    nationality = player.get("nationality", "Unknown")
    age = player["age"]
    overall = player["overall"]
    potential = player["potential"]

    card = [
        f"{border_color}╔══════════════════════════╗{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} {name} {border_color}║{RESET_COLOR}",
        f"{border_color}╠══════════════════════════╣{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Nationality: {nationality:<10} {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Age: {age:2d}{' ':16} {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Overall: {value_color}{overall:3d}{RESET_COLOR}{' ':8} {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Potential: {value_color}{potential:3d}{RESET_COLOR}{' ':10} {border_color}║{RESET_COLOR}",
        f"{border_color}╠══════════════════════════╣{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} ⚔️  Attack:    {_create_stat_bar(player['attack'])} {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} 🛡️  Defence:   {_create_stat_bar(player['defence'])} {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} 💪 Physical:   {_create_stat_bar(player['physical'])} {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} 🔧 Technique:  {_create_stat_bar(player['technique'])} {border_color}║{RESET_COLOR}",
        f"{border_color}╚══════════════════════════╝{RESET_COLOR}",
    ]

    for line in card:
        print(line)


def _create_stat_bar(value: int, max_value: int = 100, length: int = 15) -> str:
    filled = int((value / max_value) * length)
    bar = "█" * filled + "░" * (length - filled)
    if value >= 80:
        color = GREEN_COLOR
    elif value >= 60:
        color = YELLOW_COLOR
    else:
        color = RED_COLOR
    return f"{color}{bar}{RESET_COLOR} {value:3d}"


def print_players_table(players: List[Dict[str, Any]], team_name: str = "") -> None:
    if team_name:
        print(f"\n{CYAN_COLOR}=== TEAM ROSTER: {team_name} ==={RESET_COLOR}")
    else:
        print(f"\n{CYAN_COLOR}=== PLAYER LIST ==={RESET_COLOR}")

    print(
        f"{BLUE_COLOR}┌─────┬────────────────────┬────────────────────┬──────┬─────────┐{RESET_COLOR}"
    )
    print(
        f"{BLUE_COLOR}│ ID  │ Name               │ Position           │ Age  │ Rating  │{RESET_COLOR}"
    )
    print(
        f"{BLUE_COLOR}├─────┼────────────────────┼────────────────────┼──────┼─────────┤{RESET_COLOR}"
    )

    position_order = {
        "goalkeeper": 0,
        "center_back": 1,
        "fullback": 2,
        "defensive_midfielder": 3,
        "center_midfielder": 4,
        "attacking_midfielder": 5,
        "winger": 6,
        "forward": 7,
    }

    sorted_players = sorted(players, key=lambda p: position_order.get(p["position"], 8))

    for player in sorted_players:
        overall = player["overall"]
        if overall >= 85:
            rating_color = PURPLE_COLOR
        elif overall >= 75:
            rating_color = RED_COLOR
        elif overall >= 65:
            rating_color = YELLOW_COLOR
        else:
            rating_color = GREEN_COLOR

        position_translation = {
            "goalkeeper": "Goalkeeper",
            "center_back": "C. Back",
            "fullback": "Fullback",
            "defensive_midfielder": "Def. Mid",
            "center_midfielder": "C. Mid",
            "attacking_midfielder": "Att. Mid",
            "winger": "Winger",
            "forward": "Forward",
        }

        position = position_translation.get(player["position"], player["position"])
        print(
            f"{BLUE_COLOR}│{RESET_COLOR} {player['id']:3d} {BLUE_COLOR}│{RESET_COLOR} {player['name'][:18]:18} {BLUE_COLOR}│{RESET_COLOR} {position:18} {BLUE_COLOR}│{RESET_COLOR} {player['age']:4} {BLUE_COLOR}│{RESET_COLOR} {rating_color}{overall:3d}{RESET_COLOR}    {BLUE_COLOR}│{RESET_COLOR}"
        )

    print(
        f"{BLUE_COLOR}└─────┴────────────────────┴────────────────────┴──────┴─────────┘{RESET_COLOR}"
    )


def print_player_comparison(player1: Dict[str, Any], player2: Dict[str, Any]) -> None:
    print(f"\n{CYAN_COLOR}=== PLAYER COMPARISON ==={RESET_COLOR}")
    print(f"{BLUE_COLOR}┌───────────────────┬───────────────────┐{RESET_COLOR}")
    print(
        f"{BLUE_COLOR}│ {player1['name'][:17]:17} │ {player2['name'][:17]:17} {BLUE_COLOR}│{RESET_COLOR}"
    )
    print(f"{BLUE_COLOR}├───────────────────┼───────────────────┤{RESET_COLOR}")

    stats = ["attack", "defence", "physical", "technique", "speed", "stamina"]
    stat_names = ["Attack", "Defence", "Physical", "Technique", "Speed", "Stamina"]

    for stat_name, stat_key in zip(stat_names, stats):
        val1 = player1.get(stat_key, 0)
        val2 = player2.get(stat_key, 0)
        if val1 > val2:
            color1, color2 = GREEN_COLOR, RED_COLOR
        elif val1 < val2:
            color1, color2 = RED_COLOR, GREEN_COLOR
        else:
            color1 = color2 = YELLOW_COLOR

        bar1 = _create_stat_bar(val1, 100, 8)
        bar2 = _create_stat_bar(val2, 100, 8)
        print(
            f"{BLUE_COLOR}│{RESET_COLOR} {color1}{bar1} {val1:3d}{RESET_COLOR} {BLUE_COLOR}│{RESET_COLOR} {color2}{bar2} {val2:3d}{RESET_COLOR} {BLUE_COLOR}│{RESET_COLOR}"
        )

    print(f"{BLUE_COLOR}└───────────────────┴───────────────────┘{RESET_COLOR}")
