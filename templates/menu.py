CYAN_COLOR = "\033[96m"
RESET_COLOR = "\033[0m"


def print_main_menu():
    """Напечатать главное меню"""
    print(f"\n{CYAN_COLOR}ГЛАВНОЕ МЕНЮ:{RESET_COLOR}")
    print("1 - Показать турнирную сетку")
    print("2 - Показать список команд")
    print("3 - Показать список игроков")
    print("4 - Начать симуляцию матча")
    print("5 - Расширенная статистика")
    print("0 - Выход")
    print("\nВыберите опцию: ", end="")


def print_secondary_menu(context: str):
    """Напечатать второстепенное меню"""
    print(f"\nВыберите матч для деталей или 0 для возврата в {context}: ", end="")
