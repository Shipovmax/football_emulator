from typing import Any, Dict

RED_COLOR = "\033[91m"
GREEN_COLOR = "\033[92m"
RESET_COLOR = "\033[0m"


def print_tournament_ended(winner_team: Dict[str, Any]) -> None:
    print("=" * 50)
    print(f"{GREEN_COLOR}TOURNAMENT FINISHED!{RESET_COLOR}")
    print("=" * 50)
    print(f"🏆 {RED_COLOR}WINNER: {winner_team['team_name']}{RESET_COLOR} 🏆")
    print("\nThanks for using the simulator!")
    print("Press any key to exit...")
