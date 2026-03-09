YELLOW_COLOR = "\033[93m"
RESET_COLOR = "\033[0m"


def print_header():
    """Напечатать заголовок приложения"""
    line = f"{YELLOW_COLOR}Добро пожаловать в Симулятор футбола{RESET_COLOR}"
    divider_line = "-" * 40

    print(divider_line)
    print(line)
    print(divider_line)
