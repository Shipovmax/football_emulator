from typing import Any, Dict, List

GREEN_COLOR = "\033[92m"
BLUE_COLOR = "\033[94m"
YELLOW_COLOR = "\033[93m"
RED_COLOR = "\033[91m"
RESET_COLOR = "\033[0m"


def print_tournament_bracket(
    matches: List[Dict[str, Any]], teams: List[Dict[str, Any]]
) -> None:
    print(f"\n{BLUE_COLOR}TOURNAMENT BRACKET{RESET_COLOR}")
    print("=" * 50)

    quarterfinals = [m for m in matches if m["stage"] == "quarterfinal"]
    semifinals = [m for m in matches if m["stage"] == "semifinal"]
    third_place = [m for m in matches if m["stage"] == "third_place"]
    final = [m for m in matches if m["stage"] == "final"]

    if quarterfinals:
        print(f"\n{YELLOW_COLOR}QUARTERFINALS:{RESET_COLOR}")
        for match in quarterfinals:
            print_match_line(match, teams)

    if semifinals:
        print(f"\n{YELLOW_COLOR}SEMIFINALS:{RESET_COLOR}")
        for match in semifinals:
            print_match_line(match, teams)

    if third_place:
        print(f"\n{YELLOW_COLOR}THIRD PLACE MATCH:{RESET_COLOR}")
        for match in third_place:
            print_match_line(match, teams)

    if final:
        print(f"\n{YELLOW_COLOR}FINAL:{RESET_COLOR}")
        for match in final:
            print_match_line(match, teams)


def print_match_line(match: Dict[str, Any], teams: List[Dict[str, Any]]) -> None:
    home_team = next((t for t in teams if t["team_id"] == match["home_team_id"]), None)
    away_team = next((t for t in teams if t["team_id"] == match["away_team_id"]), None)
    if not home_team or not away_team:
        return

    if match["status"] == "completed":
        score = f"{match['score']['home']}-{match['score']['away']}"
        winner = home_team if match["winner_id"] == match["home_team_id"] else away_team
        print(
            f"Match {match['match_id']}: {home_team['team_name']} vs {away_team['team_name']} | {score} | Winner: {GREEN_COLOR}{winner['team_name']}{RESET_COLOR}"
        )
    else:
        print(
            f"Match {match['match_id']}: {home_team['team_name']} vs {away_team['team_name']} | {RED_COLOR}Not played{RESET_COLOR}"
        )
