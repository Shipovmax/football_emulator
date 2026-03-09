import json
import os
from typing import Any, Dict, List


class DataLoader:
    def __init__(self):
        # Определяем правильный путь к папке assets от корня проекта
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_path = os.path.join(current_dir, "assets")
        print(f"🔍 Ищем файлы в: {self.assets_path}")

    def load_players(self) -> List[Dict[str, Any]]:
        players = self._load_json("players.json")
        print(f"✅ Загружено {len(players)} игроков")
        return players

    def load_teams(self) -> List[Dict[str, Any]]:
        teams = self._load_json("teams.json")
        for team in teams:
            team["chemistry"] = self._calculate_team_chemistry(team)
            team["play_style"] = self._determine_play_style(team)
        print(f"✅ Загружено {len(teams)} команд")
        return teams

    def load_matches(self) -> List[Dict[str, Any]]:
        matches = self._load_json("matches.json")
        print(f"✅ Загружено {len(matches)} матчей")
        return matches

    def _load_json(self, filename: str) -> List[Dict[str, Any]]:
        try:
            filepath = os.path.join(self.assets_path, filename)
            print(f"🔍 Пытаемся загрузить: {filepath}")
            if not os.path.exists(filepath):
                print(f"❌ Файл {filename} не существует по пути: {filepath}")
                # Создаем пустой файл для теста
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump([], f)
                print(f"📁 Создан пустой файл: {filename}")
                return []

            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                print(f"📂 Успешно загружен {filename}")
                return data
        except FileNotFoundError:
            print(f"❌ Файл {filename} не найден по пути: {filepath}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ Ошибка JSON в {filename}: {e}")
            return []
        except Exception as e:
            print(f"❌ Неожиданная ошибка при загрузке {filename}: {e}")
            return []

    def _calculate_team_chemistry(self, team: Dict[str, Any]) -> int:
        return 85

    def _determine_play_style(self, team: Dict[str, Any]) -> str:
        styles = ["Атакующий", "Контролирующий", "Защитный", "Контратакующий"]
        return "Атакующий"


def load_all_data():
    loader = DataLoader()
    players = loader.load_players()
    teams = loader.load_teams()
    matches = loader.load_matches()
    return players, teams, matches
