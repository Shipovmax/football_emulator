import json
import os
from typing import Any, Dict, List, Tuple


class DataLoader:
    def __init__(self) -> None:
        # Resolve the assets folder path relative to the project root
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_path = os.path.join(current_dir, "assets")
        print(f"🔍 Looking for files in: {self.assets_path}")

    def load_players(self) -> List[Dict[str, Any]]:
        players = self._load_json("players.json")
        print(f"✅ Loaded {len(players)} players")
        return players

    def load_teams(self) -> List[Dict[str, Any]]:
        teams = self._load_json("teams.json")
        for team in teams:
            team["chemistry"] = self._calculate_team_chemistry(team)
            team["play_style"] = self._determine_play_style(team)
        print(f"✅ Loaded {len(teams)} teams")
        return teams

    def load_matches(self) -> List[Dict[str, Any]]:
        matches = self._load_json("matches.json")
        print(f"✅ Loaded {len(matches)} matches")
        return matches

    def _load_json(self, filename: str) -> List[Dict[str, Any]]:
        filepath = os.path.join(self.assets_path, filename)
        try:
            print(f"🔍 Attempting to load: {filepath}")
            if not os.path.exists(filepath):
                print(f"❌ File {filename} does not exist at path: {filepath}")
                # Create an empty placeholder file
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump([], f)
                print(f"📁 Created empty file: {filename}")
                return []

            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                print(f"📂 Successfully loaded {filename}")
                return data
        except FileNotFoundError:
            print(f"❌ File {filename} not found at path: {filepath}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ JSON error in {filename}: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error while loading {filename}: {e}")
            return []

    def _calculate_team_chemistry(self, team: Dict[str, Any]) -> int:
        return 85

    def _determine_play_style(self, team: Dict[str, Any]) -> str:
        # TODO: styles list is unused — play style is always "Attacking".
        styles = ["Attacking", "Possession", "Defensive", "Counter-attacking"]
        return "Attacking"


def load_all_data() -> (
    Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]
):
    loader = DataLoader()
    players = loader.load_players()
    teams = loader.load_teams()
    matches = loader.load_matches()
    return players, teams, matches
