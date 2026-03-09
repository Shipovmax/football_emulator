"""
Главный файл футбольного эмулятора с улучшенной навигацией и визуалом
"""

import os
import sys
import time

# Добавляем пути для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../templates"))

from core.data_loader import load_all_data
from core.simulation import MatchSimulator
from templates.bracket import print_tournament_bracket
from templates.header import print_header
from templates.match import print_match_details
from templates.menu import print_main_menu, print_secondary_menu
from templates.players import (
    print_player_card_ascii,
    print_player_comparison,
    print_players_table,
)
from templates.teams import print_team_card, print_teams_table

# Определяем цвета для использования в test_skip.py
GREEN_COLOR = "\033[92m"
BLUE_COLOR = "\033[94m"
YELLOW_COLOR = "\033[93m"
RED_COLOR = "\033[91m"
CYAN_COLOR = "\033[96m"
RESET_COLOR = "\033[0m"


class AdvancedFootballEmulator:
    def __init__(self):
        self.players, self.teams, self.matches = load_all_data()
        self.simulator = MatchSimulator(self.players, self.teams)
        self.current_state = "main_menu"
        self.selected_match = None
        self.selected_team = None
        self.selected_player = None

    def run(self):
        """Запуск основного цикла эмулятора"""
        print_header()
        while True:
            try:
                if self.current_state == "main_menu":
                    self.show_main_menu()
                elif self.current_state == "tournament_bracket":
                    self.show_tournament_bracket()
                elif self.current_state == "match_details":
                    self.show_match_details()
                elif self.current_state == "teams_list":
                    self.show_teams_list()
                elif self.current_state == "team_details":
                    self.show_team_details()
                elif self.current_state == "players_list":
                    self.show_players_list()
                elif self.current_state == "player_details":
                    self.show_player_details()
                elif self.current_state == "simulate_match":
                    self.simulate_match()
                else:
                    self.current_state = "main_menu"
            except KeyboardInterrupt:
                print("\n\n🔚 Выход из программы...")
                break
            except Exception as e:
                print(f"\n❌ Произошла ошибка: {e}")
                self.current_state = "main_menu"

    def show_main_menu(self):
        """Показать главное меню"""
        print_main_menu()
        choice = input().strip()

        if choice == "1":
            self.current_state = "tournament_bracket"
        elif choice == "2":
            self.current_state = "teams_list"
        elif choice == "3":
            self.current_state = "players_list"
        elif choice == "4":
            self.current_state = "simulate_match"
        elif choice == "5":
            self.show_advanced_stats()
        elif choice == "0":
            print("👋 До свидания!")
            sys.exit()
        else:
            print("❌ Неверный выбор. Попробуйте снова.")

    def show_tournament_bracket(self):
        """Показать турнирную сетку"""
        print_tournament_bracket(self.matches, self.teams)
        print_secondary_menu("главное меню")
        choice = input().strip()

        if choice == "0":
            self.current_state = "main_menu"
        elif choice.isdigit() and 1 <= int(choice) <= len(self.matches):
            match_id = int(choice)
            self.selected_match = next(
                (m for m in self.matches if m["match_id"] == match_id), None
            )
            if self.selected_match:
                self.current_state = "match_details"
            else:
                print("❌ Матч не найден!")
        else:
            print("❌ Неверный выбор!")

    def show_match_details(self):
        """Показать детали матча"""
        if not self.selected_match:
            self.current_state = "tournament_bracket"
            return

        print_match_details(self.selected_match, self.teams, self.players)

        print(f"\n{YELLOW_COLOR}ДОПОЛНИТЕЛЬНЫЕ ОПЦИИ:{RESET_COLOR}")
        print("1 - 🔄 Симулировать матч (если не сыгран)")
        print("2 - 👥 Показать составы команд")
        print("3 - 📊 Подробная статистика")
        print("0 - ↩️ Назад к сетке")
        print("\nВыберите опцию: ", end="")

        choice = input().strip()

        if choice == "1" and self.selected_match["status"] != "completed":
            # Используем текущее время как seed для случайности
            seed = int(time.time())
            self.simulator.simulate_match(self.selected_match, seed=seed)
            print("✅ Матч успешно симулирован!")
        elif choice == "2":
            self.show_match_lineups()
        elif choice == "3":
            self.show_detailed_stats()
        elif choice == "0":
            self.current_state = "tournament_bracket"
            self.selected_match = None
        else:
            print("❌ Неверный выбор!")

    def show_match_lineups(self):
        """Показать составы команд в матче"""
        if not self.selected_match:
            return

        home_team = next(
            (
                t
                for t in self.teams
                if t["team_id"] == self.selected_match["home_team_id"]
            ),
            None,
        )
        away_team = next(
            (
                t
                for t in self.teams
                if t["team_id"] == self.selected_match["away_team_id"]
            ),
            None,
        )

        print(f"\n{CYAN_COLOR}=== СОСТАВЫ КОМАНД ==={RESET_COLOR}")

        if home_team:
            home_players = [
                p for p in self.players if p["id"] in home_team["player_ids"]
            ]
            print_players_table(home_players, home_team["team_name"])

        if away_team:
            away_players = [
                p for p in self.players if p["id"] in away_team["player_ids"]
            ]
            print_players_table(away_players, away_team["team_name"])

        print(
            f"\n{YELLOW_COLOR}Выберите игрока по ID для просмотра карточки или 0 для возврата: {RESET_COLOR}",
            end="",
        )
        choice = input().strip()

        if choice == "0":
            return
        elif choice.isdigit():
            player_id = int(choice)
            player = next((p for p in self.players if p["id"] == player_id), None)
            if player:
                self.selected_player = player
                self.show_player_details()
            else:
                print("❌ Игрок не найден!")

    def show_teams_list(self):
        """Показать список всех команд"""
        print_teams_table(self.teams, self.players)

        print(
            f"\n{YELLOW_COLOR}Выберите команду по ID для деталей или 0 для возврата: {RESET_COLOR}",
            end="",
        )
        choice = input().strip()

        if choice == "0":
            self.current_state = "main_menu"
        elif choice.isdigit():
            team_id = int(choice)
            self.selected_team = next(
                (t for t in self.teams if t["team_id"] == team_id), None
            )
            if self.selected_team:
                self.current_state = "team_details"
            else:
                print("❌ Команда не найден!")
        else:
            print("❌ Неверный выбор!")

    def show_team_details(self):
        """Показать детали команды"""
        if not self.selected_team:
            self.current_state = "teams_list"
            return

        team_players = [
            p for p in self.players if p["id"] in self.selected_team["player_ids"]
        ]
        print_team_card(self.selected_team, team_players)
        print_players_table(team_players, self.selected_team["team_name"])

        print(
            f"\n{YELLOW_COLOR}Выберите игрока по ID для просмотра карточки или 0 для возврата: {RESET_COLOR}",
            end="",
        )
        choice = input().strip()

        if choice == "0":
            self.current_state = "teams_list"
            self.selected_team = None
        elif choice.isdigit():
            player_id = int(choice)
            player = next((p for p in team_players if p["id"] == player_id), None)
            if player:
                self.selected_player = player
                self.current_state = "player_details"
            else:
                print("❌ Игрок не найден!")
        else:
            print("❌ Неверный выбор!")

    def show_players_list(self):
        """Показать список всех игроков"""
        print_players_table(self.players)

        print(
            f"\n{YELLOW_COLOR}Выберите игрока по ID для просмотра карточки или 0 для возврата: {RESET_COLOR}",
            end="",
        )
        choice = input().strip()

        if choice == "0":
            self.current_state = "main_menu"
        elif choice.isdigit():
            player_id = int(choice)
            self.selected_player = next(
                (p for p in self.players if p["id"] == player_id), None
            )
            if self.selected_player:
                self.current_state = "player_details"
            else:
                print("❌ Игрок не найден!")
        else:
            print("❌ Неверный выбор!")

    def show_player_details(self):
        """Показать карточку игрока"""
        if not self.selected_player:
            self.current_state = "players_list"
            return

        print_player_card_ascii(self.selected_player)

        print(f"\n{YELLOW_COLOR}ДОПОЛНИТЕЛЬНЫЕ ОПЦИИ:{RESET_COLOR}")
        print("1 - 🔄 Сравнить с другим игроком")
        print("0 - ↩️ Назад")
        print("\nВыберите опцию: ", end="")

        choice = input().strip()

        if choice == "1":
            self.compare_players()
        elif choice == "0":
            # Возвращаемся в предыдущее состояние
            if self.selected_team:
                self.current_state = "team_details"
            else:
                self.current_state = "players_list"
            self.selected_player = None
        else:
            print("❌ Неверный выбор!")

    def compare_players(self):
        """Сравнить двух игроков"""
        print(
            f"\n{YELLOW_COLOR}Введите ID второго игрока для сравнения: {RESET_COLOR}",
            end="",
        )
        choice = input().strip()

        if choice.isdigit():
            player2_id = int(choice)
            player2 = next((p for p in self.players if p["id"] == player2_id), None)
            if player2:
                print_player_comparison(self.selected_player, player2)
                input(f"\n{YELLOW_COLOR}Нажмите Enter для продолжения...{RESET_COLOR}")
            else:
                print("❌ Игрок не найден!")
        else:
            print("❌ Неверный формат ID!")

    def simulate_match(self):
        """Симулировать выбранный матч"""
        print(f"\n{CYAN_COLOR}=== СИМУЛЯЦИЯ МАТЧА ==={RESET_COLOR}")
        print_tournament_bracket(self.matches, self.teams)

        print(
            f"\n{YELLOW_COLOR}Выберите матч для симуляции (1-{len(self.matches)}) или 0 для отмены: {RESET_COLOR}",
            end="",
        )
        choice = input().strip()

        if choice == "0":
            self.current_state = "main_menu"
            return
        elif choice.isdigit() and 1 <= int(choice) <= len(self.matches):
            match_id = int(choice)
            match = next((m for m in self.matches if m["match_id"] == match_id), None)
            if match:
                if match["status"] == "completed":
                    print(
                        "❌ Этот матч уже сыгран! Симулировать заново? (y/n): ", end=""
                    )
                    if input().strip().lower() != "y":
                        return

                print("🔄 Симулируем матч...")

                # Используем текущее время как seed для случайности
                seed = int(time.time())

                # Динамическая симуляция
                self.simulator.simulate_match(match, seed=seed)
                print("✅ Матч успешно симулирован!")
                self.selected_match = match
                self.current_state = "match_details"
            else:
                print("❌ Матч не найден!")
        else:
            print("❌ Неверный выбор!")

    def show_advanced_stats(self):
        """Показать расширенную статистику"""
        print(f"\n{CYAN_COLOR}=== РАСШИРЕННАЯ СТАТИСТИКА ==={RESET_COLOR}")

        # Топ игроков по рейтингу
        top_players = sorted(self.players, key=lambda x: x["overall"], reverse=True)[:5]
        print(f"\n{YELLOW_COLOR}🏆 ТОП-5 ИГРОКОВ ПО РЕЙТИНГУ:{RESET_COLOR}")
        for i, player in enumerate(top_players, 1):
            print(f"{i}. {player['name']} - {player['overall']} OVR")

        # Статистика команд
        print(f"\n{YELLOW_COLOR}📈 СТАТИСТИКА КОМАНД:{RESET_COLOR}")
        for team in self.teams:
            team_players = [p for p in self.players if p["id"] in team["player_ids"]]
            avg_age = sum(p["age"] for p in team_players) / len(team_players)
            avg_rating = sum(p["overall"] for p in team_players) / len(team_players)
            print(
                f"{team['team_name']}: средний возраст {avg_age:.1f}, средний рейтинг {avg_rating:.1f}"
            )

        input(f"\n{YELLOW_COLOR}Нажмите Enter для возврата...{RESET_COLOR}")

    def show_detailed_stats(self):
        """Показать детальную статистику матча"""
        if not self.selected_match or not self.selected_match.get("statistics"):
            print("❌ Статистика недоступна для этого матча!")
            return

        stats = self.selected_match["statistics"]
        print(f"\n{CYAN_COLOR}=== ДЕТАЛЬНАЯ АНАЛИТИКА МАТЧА ==={RESET_COLOR}")

        # Анализ эффективности атак
        home_shots = stats["shots"]["home"]
        home_on_target = stats["shots_on_target"]["home"]
        home_efficiency = (home_on_target / home_shots * 100) if home_shots > 0 else 0

        away_shots = stats["shots"]["away"]
        away_on_target = stats["shots_on_target"]["away"]
        away_efficiency = (away_on_target / away_shots * 100) if away_shots > 0 else 0

        print(f"\n{YELLOW_COLOR}🎯 ЭФФЕКТИВНОСТЬ АТАК:{RESET_COLOR}")
        print(
            f"Домашняя команда: {home_efficiency:.1f}% ({home_on_target}/{home_shots} в створ)"
        )
        print(
            f"Гостевая команда: {away_efficiency:.1f}% ({away_on_target}/{away_shots} в створ)"
        )

        input(f"\n{YELLOW_COLOR}Нажмите Enter для возврата...{RESET_COLOR}")


def main():
    """Главная функция запуска приложения"""
    try:
        print("🚀 Запуск футбольного эмулятора...")
        emulator = AdvancedFootballEmulator()
        emulator.run()
    except KeyboardInterrupt:
        print("\n\n🔚 Программа прервана пользователем")
    except Exception as e:
        print(f"\n💥 Критическая ошибка: {e}")


if __name__ == "__main__":
    main()
