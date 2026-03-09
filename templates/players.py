GREEN_COLOR = "\033[92m"
BLUE_COLOR = "\033[94m"
YELLOW_COLOR = "\033[93m"
RED_COLOR = "\033[91m"
PURPLE_COLOR = "\033[95m"
CYAN_COLOR = "\033[96m"
RESET_COLOR = "\033[0m"


def print_player_card_ascii(player):
    position_translation = {
        "goalkeeper": "Вратарь",
        "center_back": "Центр.защ",
        "fullback": "Крайн.защ",
        "defensive_midfielder": "Оп.полузащ",
        "center_midfielder": "Центр.полузащ",
        "attacking_midfielder": "Атак.полузащ",
        "winger": "Крайн.нап",
        "forward": "Нападающий",
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
        f"{border_color}║{RESET_COLOR} Атака:   {player['attack']:3d}       {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Защита:  {player['defence']:3d}       {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Физика:  {player['physical']:3d}       {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Техника: {player['technique']:3d}       {border_color}║{RESET_COLOR}",
        f"{border_color}╚══════════════════════╝{RESET_COLOR}",
    ]

    for line in card:
        print(line)


def print_player_card_detailed(player):
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
        f"{border_color}║{RESET_COLOR} Национальность: {nationality:<10} {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Возраст: {age:2d} лет{' ':12} {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Общий рейтинг: {value_color}{overall:3d}{RESET_COLOR}{' ':8} {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} Потенциал: {value_color}{potential:3d}{RESET_COLOR}{' ':10} {border_color}║{RESET_COLOR}",
        f"{border_color}╠══════════════════════════╣{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} ⚔️  Атака:    {_create_stat_bar(player['attack'])} {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} 🛡️  Защита:   {_create_stat_bar(player['defence'])} {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} 💪 Физика:    {_create_stat_bar(player['physical'])} {border_color}║{RESET_COLOR}",
        f"{border_color}║{RESET_COLOR} 🔧 Техника:   {_create_stat_bar(player['technique'])} {border_color}║{RESET_COLOR}",
        f"{border_color}╚══════════════════════════╝{RESET_COLOR}",
    ]

    for line in card:
        print(line)


def _create_stat_bar(value, max_value=100, length=15):
    filled = int((value / max_value) * length)
    bar = "█" * filled + "░" * (length - filled)
    if value >= 80:
        color = GREEN_COLOR
    elif value >= 60:
        color = YELLOW_COLOR
    else:
        color = RED_COLOR
    return f"{color}{bar}{RESET_COLOR} {value:3d}"


def print_players_table(players: list, team_name: str = ""):
    if team_name:
        print(f"\n{CYAN_COLOR}=== СОСТАВ КОМАНДЫ: {team_name} ==={RESET_COLOR}")
    else:
        print(f"\n{CYAN_COLOR}=== СПИСОК ИГРОКОВ ==={RESET_COLOR}")

    print(
        f"{BLUE_COLOR}┌─────┬────────────────────┬────────────────────┬──────┬─────────┐{RESET_COLOR}"
    )
    print(
        f"{BLUE_COLOR}│ ID  │ Имя                │ Позиция            │ Возр.│ Рейтинг │{RESET_COLOR}"
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
            "goalkeeper": "Вратарь",
            "center_back": "Ц.Защитник",
            "fullback": "Кр.Защитник",
            "defensive_midfielder": "Оп.Полузащ",
            "center_midfielder": "Ц.Полузащ",
            "attacking_midfielder": "Ат.Полузащ",
            "winger": "Крайний нап.",
            "forward": "Нападающий",
        }

        position = position_translation.get(player["position"], player["position"])
        print(
            f"{BLUE_COLOR}│{RESET_COLOR} {player['id']:3d} {BLUE_COLOR}│{RESET_COLOR} {player['name'][:18]:18} {BLUE_COLOR}│{RESET_COLOR} {position:18} {BLUE_COLOR}│{RESET_COLOR} {player['age']:4} {BLUE_COLOR}│{RESET_COLOR} {rating_color}{overall:3d}{RESET_COLOR}    {BLUE_COLOR}│{RESET_COLOR}"
        )

    print(
        f"{BLUE_COLOR}└─────┴────────────────────┴────────────────────┴──────┴─────────┘{RESET_COLOR}"
    )


def print_player_comparison(player1: dict, player2: dict):
    print(f"\n{CYAN_COLOR}=== СРАВНЕНИЕ ИГРОКОВ ==={RESET_COLOR}")
    print(f"{BLUE_COLOR}┌───────────────────┬───────────────────┐{RESET_COLOR}")
    print(
        f"{BLUE_COLOR}│ {player1['name'][:17]:17} │ {player2['name'][:17]:17} {BLUE_COLOR}│{RESET_COLOR}"
    )
    print(f"{BLUE_COLOR}├───────────────────┼───────────────────┤{RESET_COLOR}")

    stats = ["attack", "defence", "physical", "technique", "speed", "stamina"]
    stat_names = ["Атака", "Защита", "Физика", "Техника", "Скорость", "Выносливость"]

    for stat_name_ru, stat_key in zip(stat_names, stats):
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
