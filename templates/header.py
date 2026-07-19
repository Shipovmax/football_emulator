YELLOW_COLOR = "\033[93m"
RESET_COLOR = "\033[0m"


def print_header() -> None:
    """Print the application header."""
    line = f"{YELLOW_COLOR}Welcome to Football Emulator{RESET_COLOR}"
    divider_line = "-" * 40

    print(divider_line)
    print(line)
    print(divider_line)
