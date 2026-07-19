from typing import Any, Dict, List

GREEN_COLOR = "\033[92m"
BLUE_COLOR = "\033[94m"
YELLOW_COLOR = "\033[93m"
RED_COLOR = "\033[91m"
CYAN_COLOR = "\033[96m"
RESET_COLOR = "\033[0m"


def print_team_card(team: Dict[str, Any], players: List[Dict[str, Any]]) -> None:
    team_players = [p for p in players if p["id"] in team["player_ids"]]
    avg_overall = (
        sum(p["overall"] for p in team_players) / len(team_players)
        if team_players
        else 0
    )
    attack_power = calculate_team_attack_power(team_players)
    defense_power = calculate_team_defense_power(team_players)

    print(f"\n{CYAN_COLOR}┌──────────────────────────────────┐{RESET_COLOR}")
    print(
        f"{CYAN_COLOR}│{RESET_COLOR} {team['team_name']:^32} {CYAN_COLOR}│{RESET_COLOR}"
    )
    print(f"{CYAN_COLOR}├──────────────────────────────────┤{RESET_COLOR}")
    print(
        f"{CYAN_COLOR}│{RESET_COLOR} Team chemistry: {team.get('chemistry', 0):3d}/100{' ':11} {CYAN_COLOR}│{RESET_COLOR}"
    )
    print(
        f"{CYAN_COLOR}│{RESET_COLOR} Play style: {team.get('play_style', 'Attacking'):<18} {CYAN_COLOR}│{RESET_COLOR}"
    )
    print(
        f"{CYAN_COLOR}│{RESET_COLOR} Average rating: {avg_overall:5.1f}{' ':10} {CYAN_COLOR}│{RESET_COLOR}"
    )
    print(f"{CYAN_COLOR}├──────────────────────────────────┤{RESET_COLOR}")
    print(
        f"{CYAN_COLOR}│{RESET_COLOR} Attack power:  {create_stat_bar(attack_power)}{attack_power:3d} {CYAN_COLOR}│{RESET_COLOR}"
    )
    print(
        f"{CYAN_COLOR}│{RESET_COLOR} Defense power: {create_stat_bar(defense_power)}{defense_power:3d} {CYAN_COLOR}│{RESET_COLOR}"
    )
    print(
        f"{CYAN_COLOR}│{RESET_COLOR} Overall power: {create_stat_bar(team.get('power', 0))}{team.get('power', 0):3d} {CYAN_COLOR}│{RESET_COLOR}"
    )
    print(f"{CYAN_COLOR}├──────────────────────────────────┤{RESET_COLOR}")
    print(f"{CYAN_COLOR}│{RESET_COLOR} Roster:{' ':25} {CYAN_COLOR}│{RESET_COLOR}")

    positions = {}
    for player in team_players:
        pos = player["position"]
        positions[pos] = positions.get(pos, 0) + 1

    position_names = {
        "goalkeeper": "Goalkeepers",
        "center_back": "Center backs",
        "fullback": "Fullbacks",
        "defensive_midfielder": "Defensive midfielders",
        "center_midfielder": "Center midfielders",
        "attacking_midfielder": "Attacking midfielders",
        "winger": "Wingers",
        "forward": "Forwards",
    }

    for pos_key, pos_name in position_names.items():
        count = positions.get(pos_key, 0)
        if count > 0:
            print(
                f"{CYAN_COLOR}│{RESET_COLOR} • {pos_name}: {count:2d}{' ':18} {CYAN_COLOR}│{RESET_COLOR}"
            )

    print(f"{CYAN_COLOR}└──────────────────────────────────┘{RESET_COLOR}")


def calculate_team_attack_power(players: List[Dict[str, Any]]) -> int:
    attacking_positions = ["forward", "winger", "attacking_midfielder"]
    attacking_players = [p for p in players if p["position"] in attacking_positions]
    if not attacking_players:
        return 50
    total_attack = sum(
        p["attack"] + p["technique"] + p.get("speed", 50) for p in attacking_players
    )
    return min(100, int(total_attack / (len(attacking_players) * 3)))


def calculate_team_defense_power(players: List[Dict[str, Any]]) -> int:
    defending_positions = [
        "goalkeeper",
        "center_back",
        "fullback",
        "defensive_midfielder",
    ]
    defending_players = [p for p in players if p["position"] in defending_positions]
    if not defending_players:
        return 50
    total_defense = sum(
        p["defence"] + p["physical"] + p.get("mentality", 50) for p in defending_players
    )
    return min(100, int(total_defense / (len(defending_players) * 3)))


def create_stat_bar(value: int, max_value: int = 100, length: int = 10) -> str:
    filled = int((value / max_value) * length)
    bar = "█" * filled + "▁" * (length - filled)
    if value >= 80:
        color = GREEN_COLOR
    elif value >= 60:
        color = YELLOW_COLOR
    else:
        color = RED_COLOR
    return f"{color}{bar}{RESET_COLOR}"


def print_teams_table(teams: List[Dict[str, Any]], players: List[Dict[str, Any]]) -> None:
    print(f"\n{CYAN_COLOR}=== TEAM LIST ==={RESET_COLOR}")
    print(
        f"{BLUE_COLOR}┌─────┬────────────────────┬─────────┬─────────┬─────────┬──────────┐{RESET_COLOR}"
    )
    print(
        f"{BLUE_COLOR}│ ID  │ Name               │ Players │ Attack  │ Defence │ Chemistry│{RESET_COLOR}"
    )
    print(
        f"{BLUE_COLOR}├─────┼────────────────────┼─────────┼─────────┼─────────┼──────────┤{RESET_COLOR}"
    )

    for team in teams:
        team_players = [p for p in players if p["id"] in team["player_ids"]]
        attack_power = calculate_team_attack_power(team_players)
        defense_power = calculate_team_defense_power(team_players)
        chemistry = team.get("chemistry", 0)

        attack_color = (
            GREEN_COLOR
            if attack_power >= 70
            else YELLOW_COLOR
            if attack_power >= 50
            else RED_COLOR
        )
        defense_color = (
            GREEN_COLOR
            if defense_power >= 70
            else YELLOW_COLOR
            if defense_power >= 50
            else RED_COLOR
        )
        chemistry_color = (
            GREEN_COLOR
            if chemistry >= 80
            else YELLOW_COLOR
            if chemistry >= 60
            else RED_COLOR
        )

        print(
            f"{BLUE_COLOR}│{RESET_COLOR} {team['team_id']:3d} {BLUE_COLOR}│{RESET_COLOR} {team['team_name'][:18]:18} {BLUE_COLOR}│{RESET_COLOR} {len(team_players):7d} {BLUE_COLOR}│{RESET_COLOR} {attack_color}{attack_power:3d}{RESET_COLOR}    {BLUE_COLOR}│{RESET_COLOR} {defense_color}{defense_power:3d}{RESET_COLOR}    {BLUE_COLOR}│{RESET_COLOR} {chemistry_color}{chemistry:3d}{RESET_COLOR}/100 {BLUE_COLOR}│{RESET_COLOR}"
        )

    print(
        f"{BLUE_COLOR}└─────┴────────────────────┴─────────┴─────────┴─────────┴──────────┘{RESET_COLOR}"
    )
