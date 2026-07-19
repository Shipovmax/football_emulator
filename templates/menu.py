CYAN_COLOR = "\033[96m"
RESET_COLOR = "\033[0m"


def print_main_menu() -> None:
    """Print the main menu."""
    print(f"\n{CYAN_COLOR}MAIN MENU:{RESET_COLOR}")
    print("1 - Show tournament bracket")
    print("2 - Show team list")
    print("3 - Show player list")
    print("4 - Start match simulation")
    print("5 - Advanced statistics")
    print("0 - Exit")
    print("\nChoose an option: ", end="")


def print_secondary_menu(context: str) -> None:
    """Print a secondary menu."""
    print(f"\nSelect a match for details or 0 to return to {context}: ", end="")
