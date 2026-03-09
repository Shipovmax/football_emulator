import math
import random
from typing import Dict, List


class PlayerCalculator:
    def calculate_player_value(self, player):
        base_value = player["overall"] * 10000
        age_modifier = self._calculate_age_modifier(player["age"])
        potential_modifier = (player["potential"] - player["overall"]) * 5000
        rarity_bonus = self._calculate_rarity_bonus(player)
        traits_bonus = len(player.get("traits", [])) * 15000

        total_value = (
            base_value * age_modifier + potential_modifier + rarity_bonus + traits_bonus
        )
        return max(10000, int(total_value))

    def _calculate_age_modifier(self, age):
        if age <= 21:
            return 0.7
        elif age <= 23:
            return 0.85
        elif age <= 26:
            return 1.0
        elif age <= 29:
            return 0.95
        elif age <= 32:
            return 0.8
        else:
            return 0.6

    def _calculate_rarity_bonus(self, player):
        bonus = 0
        if player["position"] in ["forward", "winger"] and player["defence"] > 70:
            bonus += 20000
        if player["position"] in ["center_back", "fullback"] and player["attack"] > 70:
            bonus += 25000
        stats = [
            player["attack"],
            player["defence"],
            player["physical"],
            player["technique"],
        ]
        if max(stats) - min(stats) < 15:
            bonus += 15000
        return bonus


class ChemistryCalculator:
    def calculate_team_chemistry(self, team_players):
        if len(team_players) < 11:
            return 50
        nationality_score = self._calculate_nationality_bonus(team_players)
        age_balance_score = self._calculate_age_balance(team_players)
        playing_style_score = self._calculate_playing_style_compatibility(team_players)
        experience_score = self._calculate_experience_bonus(team_players)

        total_chemistry = (
            nationality_score * 0.3
            + age_balance_score * 0.25
            + playing_style_score * 0.25
            + experience_score * 0.2
        )
        return min(100, int(total_chemistry))

    def _calculate_nationality_bonus(self, players):
        nationalities = {}
        for player in players:
            nationality = player["nationality"]
            nationalities[nationality] = nationalities.get(nationality, 0) + 1
        most_common = max(nationalities.values())
        bonus = (most_common / len(players)) * 100
        return bonus

    def _calculate_age_balance(self, players):
        ages = [player["age"] for player in players]
        avg_age = sum(ages) / len(ages)
        if 25 <= avg_age <= 28:
            return 100
        elif 23 <= avg_age < 25 or 28 < avg_age <= 30:
            return 80
        elif 21 <= avg_age < 23 or 30 < avg_age <= 32:
            return 60
        else:
            return 40


class MatchCalculator:
    def __init__(self, players: List[Dict]):
        self.players = players

    def calculate_team_power(self, team: Dict) -> float:
        team_players = [p for p in self.players if p["id"] in team["player_ids"]]
        if not team_players:
            return 0
        base_power = sum(p["overall"] for p in team_players) / len(team_players)
        chemistry_bonus = team.get("chemistry", 50) / 100
        balance_bonus = self._calculate_balance_bonus(team_players)
        synergy_bonus = self._calculate_synergy_bonus(team_players)
        total_power = base_power * (
            1 + chemistry_bonus * 0.2 + balance_bonus + synergy_bonus
        )
        return round(total_power, 2)

    def _calculate_balance_bonus(self, players: List[Dict]) -> float:
        positions = {}
        for player in players:
            pos = player["position"]
            positions[pos] = positions.get(pos, 0) + 1
        ideal_distribution = {
            "goalkeeper": 1,
            "center_back": 2,
            "fullback": 2,
            "defensive_midfielder": 1,
            "center_midfielder": 2,
            "attacking_midfielder": 1,
            "winger": 2,
            "forward": 1,
        }
        balance_score = 0
        for pos, ideal_count in ideal_distribution.items():
            actual_count = positions.get(pos, 0)
            balance_score += 1 - min(1, abs(actual_count - ideal_count) / ideal_count)
        return balance_score / len(ideal_distribution) * 0.1

    def _calculate_synergy_bonus(self, players: List[Dict]) -> float:
        total_speed = sum(p.get("speed", 50) for p in players)
        total_technique = sum(p.get("technique", 50) for p in players)
        total_physical = sum(p.get("physical", 50) for p in players)
        avg_speed = total_speed / len(players)
        avg_technique = total_technique / len(players)
        avg_physical = total_physical / len(players)
        synergy = min(avg_speed, avg_technique, avg_physical) / max(
            avg_speed, avg_technique, avg_physical
        )
        return synergy * 0.05


class ProbabilityCalculator:
    @staticmethod
    def calculate_goal_probability(
        attacker: Dict, defender: Dict, goalkeeper: Dict
    ) -> float:
        attacker_rating = (attacker["attack"] + attacker["technique"]) / 2
        defender_rating = defender["defence"] if defender else 50
        goalkeeper_rating = goalkeeper["defence"]
        base_probability = attacker_rating / 100
        distance_modifier = 0.8
        angle_modifier = 0.9
        pressure_modifier = 0.7
        defense_strength = (defender_rating + goalkeeper_rating) / 200
        probability = (
            base_probability
            * distance_modifier
            * angle_modifier
            * pressure_modifier
            * (1 - defense_strength)
        )
        return max(0.05, min(0.8, probability))
