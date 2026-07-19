from typing import Any, Dict, List

GREEN_COLOR = "\033[92m"
YELLOW_COLOR = "\033[93m"
RESET_COLOR = "\033[0m"


def print_match_timeline(match: Dict[str, Any], teams: List[Dict[str, Any]], players: List[Dict[str, Any]]) -> None:
    home_team = next(team for team in teams if team["team_id"] == match["home_team_id"])
    away_team = next(team for team in teams if team["team_id"] == match["away_team_id"])

    print(f"{home_team['team_name']}")
    print("|")
    print(f"/Match {match['match_id']}/")
    print("|")
    print(f"{away_team['team_name']}")
    print()

    if match["goals"]:
        print(f"{YELLOW_COLOR}GOALS IN THE MATCH:{RESET_COLOR}")
        for goal in sorted(match["goals"], key=lambda x: x["minute"]):
            scoring_team = (
                home_team if goal["team_id"] == match["home_team_id"] else away_team
            )
            conceding_team = (
                away_team if goal["team_id"] == match["home_team_id"] else home_team
            )
            player = next(p for p in players if p["id"] == goal["player_id"])

            print(
                f"{GREEN_COLOR}{goal['minute']}'{RESET_COLOR} - {scoring_team['team_name']} ({player['name']}) against {conceding_team['team_name']}"
            )
            print(f"   {goal['description']}")
    else:
        print("No goals were scored in this match")

    print("\nExit match (Press 1)")
    print("Return to bracket (Press 2)")
