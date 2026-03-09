RED_COLOR = "\033[91m"
GREEN_COLOR = "\033[92m"
RESET_COLOR = "\033[0m"


def print_tournament_ended(winner_team):
    print("=" * 50)
    print(f"{GREEN_COLOR}ТУРНИР ЗАВЕРШЕН!{RESET_COLOR}")
    print("=" * 50)
    print(f"🏆 {RED_COLOR}ПОБЕДИТЕЛЬ: {winner_team['team_name']}{RESET_COLOR} 🏆")
    print("\nСпасибо за использование симулятора!")
    print("Для выхода нажмите любую клавишу...")
