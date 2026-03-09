GREEN_COLOR = "\033[92m"
BLUE_COLOR = "\033[94m"
YELLOW_COLOR = "\033[93m"
RED_COLOR = "\033[91m"
CYAN_COLOR = "\033[96m"
RESET_COLOR = "\033[0m"


def print_match_details(match: dict, teams: list, players: list):
    home_team = next((t for t in teams if t["team_id"] == match["home_team_id"]), None)
    away_team = next((t for t in teams if t["team_id"] == match["away_team_id"]), None)
    if not home_team or not away_team:
        print("❌ Ошибка: команды не найдены!")
        return

    print(f"\n{CYAN_COLOR}=== ДЕТАЛИ МАТЧА ==={RESET_COLOR}")
    print(f"{BLUE_COLOR}┌──────────────────────────────────┐{RESET_COLOR}")
    print(
        f"{BLUE_COLOR}│{RESET_COLOR} Матч #{match['match_id']:2d} {' ':20} {BLUE_COLOR}│{RESET_COLOR}"
    )
    print(
        f"{BLUE_COLOR}│{RESET_COLOR} {match.get('stage', 'Групповой этап'):^30} {BLUE_COLOR}│{RESET_COLOR}"
    )
    print(f"{BLUE_COLOR}├──────────────────────────────────┤{RESET_COLOR}")

    if match["status"] == "completed":
        home_score = match["score"]["home"]
        away_score = match["score"]["away"]
        if home_score > away_score:
            home_color, away_color = GREEN_COLOR, RED_COLOR
        elif home_score < away_score:
            home_color, away_color = RED_COLOR, GREEN_COLOR
        else:
            home_color = away_color = YELLOW_COLOR

        print(
            f"{BLUE_COLOR}│{RESET_COLOR} {home_team['team_name'][:15]:15} {home_color}{home_score:2d}{RESET_COLOR} - {away_color}{away_score:2d}{RESET_COLOR} {away_team['team_name'][:15]:15} {BLUE_COLOR}│{RESET_COLOR}"
        )

        if match.get("winner_id"):
            winner = (
                home_team if match["winner_id"] == home_team["team_id"] else away_team
            )
            print(
                f"{BLUE_COLOR}│{RESET_COLOR} Победитель: {GREEN_COLOR}{winner['team_name']:<18}{RESET_COLOR} {BLUE_COLOR}│{RESET_COLOR}"
            )
    else:
        print(
            f"{BLUE_COLOR}│{RESET_COLOR} {home_team['team_name'][:15]:15} {' vs '} {away_team['team_name'][:15]:15} {BLUE_COLOR}│{RESET_COLOR}"
        )
        print(
            f"{BLUE_COLOR}│{RESET_COLOR} {'МАТЧ ЕЩЕ НЕ СОСТОЯЛСЯ':^30} {BLUE_COLOR}│{RESET_COLOR}"
        )

    print(f"{BLUE_COLOR}└──────────────────────────────────┘{RESET_COLOR}")

    if match.get("statistics"):
        print_match_statistics(match["statistics"], home_team, away_team)

    if match.get("events"):
        print_match_events(match["events"], teams, players)


def print_match_statistics(stats: dict, home_team: dict, away_team: dict):
    print(f"\n{YELLOW_COLOR}📊 СТАТИСТИКА МАТЧА:{RESET_COLOR}")
    print(f"{BLUE_COLOR}┌──────────────────┬──────────┬──────────┐{RESET_COLOR}")
    print(
        f"{BLUE_COLOR}│ Показатель       │ {home_team['team_name'][:8]:8} │ {away_team['team_name'][:8]:8} {BLUE_COLOR}│{RESET_COLOR}"
    )
    print(f"{BLUE_COLOR}├──────────────────┼──────────┼──────────┤{RESET_COLOR}")

    statistics = [
        ("Владение мячом", "possession", "%"),
        ("Удары", "shots", ""),
        ("Удары в створ", "shots_on_target", ""),
        ("Угловые", "corners", ""),
        ("Фолы", "fouls", ""),
    ]

    for stat_name, stat_key, suffix in statistics:
        if stat_key in stats:
            home_val = stats[stat_key]["home"]
            away_val = stats[stat_key]["away"]
            home_color = (
                GREEN_COLOR
                if home_val > away_val
                else RED_COLOR
                if home_val < away_val
                else YELLOW_COLOR
            )
            away_color = (
                GREEN_COLOR
                if away_val > home_val
                else RED_COLOR
                if away_val < home_val
                else YELLOW_COLOR
            )
            print(
                f"{BLUE_COLOR}│{RESET_COLOR} {stat_name:<16} {BLUE_COLOR}│{RESET_COLOR} {home_color}{home_val:3d}{suffix:1} {RESET_COLOR} {BLUE_COLOR}│{RESET_COLOR} {away_color}{away_val:3d}{suffix:1} {RESET_COLOR} {BLUE_COLOR}│{RESET_COLOR}"
            )

    print(f"{BLUE_COLOR}└──────────────────┴──────────┴──────────┘{RESET_COLOR}")


def print_match_events(events: list, teams: list, players: list):
    print(f"\n{YELLOW_COLOR}⏰ ХРОНОЛОГИЯ СОБЫТИЙ:{RESET_COLOR}")
    print(
        f"{BLUE_COLOR}┌──────┬──────────┬────────────────────────────────┐{RESET_COLOR}"
    )
    print(
        f"{BLUE_COLOR}│ Минута │ Тип      │ Описание                      │{RESET_COLOR}"
    )
    print(
        f"{BLUE_COLOR}├──────┼──────────┼────────────────────────────────┤{RESET_COLOR}"
    )

    for event in events:
        minute = event["minute"]
        event_type = event["type"]
        team = next((t for t in teams if t["team_id"] == event["team_id"]), None)

        if event_type == "goal":
            icon, color, event_type_name = "⚽", GREEN_COLOR, "Гол"
        elif event_type == "shot":
            icon, color, event_type_name = "🎯", YELLOW_COLOR, "Удар"
        elif event_type == "foul":
            icon, color, event_type_name = "💥", RED_COLOR, "Фол"
        elif event_type == "corner":
            icon, color, event_type_name = "↩️", BLUE_COLOR, "Угловой"
        elif event_type == "yellow_card":
            icon, color, event_type_name = "🟨", YELLOW_COLOR, "Желтая"
        else:
            icon, color, event_type_name = "🔹", CYAN_COLOR, event_type

        description = event.get("description", "")
        if event.get("player_id"):
            player = next((p for p in players if p["id"] == event["player_id"]), None)
            if player:
                description = f"{player['name']} - {description}"

        if len(description) > 30:
            description = description[:27] + "..."
        print(
            f"{BLUE_COLOR}│{RESET_COLOR} {minute:3d}'  {BLUE_COLOR}│{RESET_COLOR} {color}{icon} {event_type_name:<6}{RESET_COLOR} {BLUE_COLOR}│{RESET_COLOR} {description:<30} {BLUE_COLOR}│{RESET_COLOR}"
        )

    print(
        f"{BLUE_COLOR}└──────┴──────────┴────────────────────────────────┘{RESET_COLOR}"
    )
