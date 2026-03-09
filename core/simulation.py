import random
import time
from typing import Dict, List, Tuple

from .calculators import MatchCalculator, ProbabilityCalculator


class MatchSimulator:
    def __init__(self, players: List[Dict], teams: List[Dict]):
        self.players = players
        self.teams = teams
        self.calculator = MatchCalculator(players)
        self.prob_calculator = ProbabilityCalculator()

    def simulate_match(self, match: Dict, seed: int = None) -> Dict:
        """Провести симуляцию матча с динамической генерацией событий"""
        if seed is not None:
            random.seed(seed)

        home_team = self._find_team(match["home_team_id"])
        away_team = self._find_team(match["away_team_id"])

        if not home_team or not away_team:
            return match

        # Расчет сил команд для симуляции
        home_power = self.calculator.calculate_team_power(home_team)
        away_power = self.calculator.calculate_team_power(away_team)

        # Генерация событий матча
        events = self._simulate_match_events(
            home_team, away_team, home_power, away_power
        )

        # Расчет счета и статистики
        score = self._calculate_score(
            events, home_team["team_id"], away_team["team_id"]
        )
        statistics = self._calculate_statistics(
            events, home_team["team_id"], away_team["team_id"]
        )

        # Определение победителя
        winner_id = self._determine_winner(
            score, home_team["team_id"], away_team["team_id"]
        )

        # Обновление данных матча
        match.update(
            {
                "status": "completed",
                "score": score,
                "events": events,
                "statistics": statistics,
                "winner_id": winner_id,
            }
        )

        return match

    def _simulate_match_events(
        self, home_team: Dict, away_team: Dict, home_power: float, away_power: float
    ) -> List[Dict]:
        """Динамическая симуляция событий матча"""
        events = []
        home_score = 0
        away_score = 0

        # Баланс сил с учетом домашнего преимущества
        home_advantage = 1.15
        total_power = home_power * home_advantage + away_power
        home_attack_prob = (home_power * home_advantage) / total_power
        away_attack_prob = away_power / total_power

        # Симуляция по минутам (1-90)
        for minute in range(1, 91):
            # Интенсивность атак в зависимости от минуты
            intensity = self._get_minute_intensity(minute)

            # Определяем, какая команда атакует
            if random.random() < intensity:
                if random.random() < home_attack_prob:
                    # Атака домашней команды
                    event = self._simulate_attack(home_team, away_team, minute, "home")
                    if event:
                        events.append(event)
                        if event["type"] == "goal":
                            home_score += 1
                else:
                    # Атака гостевой команды
                    event = self._simulate_attack(away_team, home_team, minute, "away")
                    if event:
                        events.append(event)
                        if event["type"] == "goal":
                            away_score += 1

            # Шанс на событие без атаки (фол, карточка)
            if random.random() < 0.1:
                event = self._simulate_non_attack_event(
                    home_team, away_team, minute, home_attack_prob
                )
                if event:
                    events.append(event)

        return sorted(events, key=lambda x: x["minute"])

    def _simulate_attack(
        self, attacking_team: Dict, defending_team: Dict, minute: int, side: str
    ) -> Dict:
        """Симуляция одной атаки"""
        # Выбор атакующего игрока
        attacker = self._select_attacking_player(attacking_team)
        if not attacker:
            return None

        # Выбор защитника и вратаря
        defender = self._select_defending_player(defending_team)
        goalkeeper = self._select_goalkeeper(defending_team)

        if not goalkeeper:
            return None

        # Расчет вероятности гола
        goal_probability = self.prob_calculator.calculate_goal_probability(
            attacker, defender, goalkeeper
        )

        # Модификаторы
        minute_modifier = self._get_minute_pressure(minute)
        final_probability = goal_probability * minute_modifier

        # Определение исхода атаки
        if random.random() < final_probability:
            # ГОООЛ!
            return self._create_goal_event(
                attacking_team, defending_team, attacker, minute, side
            )
        elif random.random() < 0.3:
            # Удар мимо/блокирован
            return self._create_shot_event(
                attacking_team, attacker, minute, side, on_target=False
            )
        elif random.random() < 0.4:
            # Удар в створ (сейв)
            return self._create_shot_event(
                attacking_team, attacker, minute, side, on_target=True
            )
        elif random.random() < 0.2:
            # Фол при атаке
            return self._create_foul_event(defending_team, minute, side)

        return None

    def _simulate_non_attack_event(
        self, home_team: Dict, away_team: Dict, minute: int, home_attack_prob: float
    ) -> Dict:
        """Симуляция события без атаки (фол, угловой и т.д.)"""
        event_type = random.choices(
            ["foul", "corner", "yellow_card", "offside"], weights=[0.5, 0.3, 0.15, 0.05]
        )[0]

        # Определяем команду
        if random.random() < home_attack_prob:
            team = home_team
            side = "home"
        else:
            team = away_team
            side = "away"

        if event_type == "foul":
            return self._create_foul_event(team, minute, side)
        elif event_type == "corner":
            return self._create_corner_event(team, minute, side)
        elif event_type == "yellow_card":
            player = self._select_random_player(team)
            return {
                "minute": minute,
                "type": "yellow_card",
                "team_id": team["team_id"],
                "player_id": player["id"] if player else None,
                "description": f"Желтая карточка за грубую игру",
            }
        elif event_type == "offside":
            return {
                "minute": minute,
                "type": "offside",
                "team_id": team["team_id"],
                "description": "Положение вне игры",
            }

        return None

    def _select_attacking_player(self, team: Dict) -> Dict:
        """Выбор атакующего игрока с приоритетом по позициям"""
        positions = ["forward", "winger", "attacking_midfielder", "center_midfielder"]
        for position in positions:
            players = [
                p
                for p in self.players
                if p["id"] in team["player_ids"] and p["position"] == position
            ]
            if players:
                # Вес выбора на основе атаки
                weights = [p["attack"] for p in players]
                return random.choices(players, weights=weights)[0]
        return self._select_random_player(team)

    def _select_defending_player(self, team: Dict) -> Dict:
        """Выбор защищающегося игрока"""
        positions = ["center_back", "fullback", "defensive_midfielder"]
        for position in positions:
            players = [
                p
                for p in self.players
                if p["id"] in team["player_ids"] and p["position"] == position
            ]
            if players:
                weights = [p["defence"] for p in players]
                return random.choices(players, weights=weights)[0]
        return self._select_random_player(team)

    def _select_goalkeeper(self, team: Dict) -> Dict:
        """Выбор вратаря"""
        goalkeepers = [
            p
            for p in self.players
            if p["id"] in team["player_ids"] and p["position"] == "goalkeeper"
        ]
        return random.choice(goalkeepers) if goalkeepers else None

    def _select_random_player(self, team: Dict) -> Dict:
        """Случайный выбор игрока из команды"""
        team_players = [p for p in self.players if p["id"] in team["player_ids"]]
        return random.choice(team_players) if team_players else None

    def _create_goal_event(
        self,
        attacking_team: Dict,
        defending_team: Dict,
        scorer: Dict,
        minute: int,
        side: str,
    ) -> Dict:
        """Создание события гола"""
        goal_types = ["open_play", "header", "long_shot", "penalty", "free_kick"]
        goal_type = random.choices(goal_types, weights=[0.6, 0.15, 0.15, 0.05, 0.05])[0]

        # Возможный ассистент
        assister = None
        if random.random() < 0.7:  # 70% голов с передачей
            assister = self._select_attacking_player(attacking_team)
            while assister and assister["id"] == scorer["id"]:
                assister = self._select_attacking_player(attacking_team)

        descriptions = {
            "open_play": [
                f"Красивый удар из-за пределов штрафной!",
                f"Хладнокровно переиграл вратаря!",
                f"Мощный удар в ближний угол!",
                f"Точный удар низом!",
            ],
            "header": [
                f"Великолепный удар головой!",
                f"Выскочил на подачу и замкнул передачу!",
                f"Сильный удар головой из-за линии вратаря!",
            ],
            "long_shot": [
                f"Невероятный гол дальним ударом!",
                f"Бьюет издали... ГОООЛ!",
                f"Мощный удар из-за пределов штрафной!",
            ],
            "penalty": [
                f"Точно пробитый пенальти!",
                f"Хладнокровно реализовал пенальти!",
                f"Вратарь угадал, но не достал!",
            ],
            "free_kick": [
                f"Великолепный гол со штрафного!",
                f"Бьюет... Штанга... ГОООЛ!",
                f"Неберущийся штрафной удар!",
            ],
        }

        description = random.choice(descriptions[goal_type])
        if assister:
            description = (
                f"{assister['name']} отдает передачу на {scorer['name']}. {description}"
            )
        else:
            description = f"{scorer['name']}. {description}"

        return {
            "minute": minute,
            "type": "goal",
            "team_id": attacking_team["team_id"],
            "player_id": scorer["id"],
            "assist_player_id": assister["id"] if assister else None,
            "goal_type": goal_type,
            "description": description,
        }

    def _create_shot_event(
        self, team: Dict, shooter: Dict, minute: int, side: str, on_target: bool
    ) -> Dict:
        """Создание события удара"""
        descriptions_on = [
            "Мощный удар в створ!",
            "Опасный момент! Удар по воротам!",
            "Пытается пробить из-за штрафной!",
        ]
        descriptions_off = [
            "Удар мимо ворот!",
            "Бьет выше перекладины!",
            "Промах по воротам!",
        ]

        description = random.choice(descriptions_on if on_target else descriptions_off)

        return {
            "minute": minute,
            "type": "shot",
            "team_id": team["team_id"],
            "player_id": shooter["id"],
            "on_target": on_target,
            "description": f"{shooter['name']}. {description}",
        }

    def _create_foul_event(self, team: Dict, minute: int, side: str) -> Dict:
        """Создание события фола"""
        fouler = self._select_random_player(team)
        descriptions = ["Жесткий подкат!", "Нарушение правил!", "Грубая игра!"]

        # Шанс на карточку
        card = None
        if random.random() < 0.3:
            card = "yellow" if random.random() < 0.9 else "red"

        return {
            "minute": minute,
            "type": "foul",
            "team_id": team["team_id"],
            "player_id": fouler["id"] if fouler else None,
            "card": card,
            "description": f"{random.choice(descriptions)} {fouler['name'] if fouler else 'Игрок'} получает {'желтую' if card == 'yellow' else 'красную' if card == 'red' else 'предупреждение'}.",
        }

    def _create_corner_event(self, team: Dict, minute: int, side: str) -> Dict:
        """Создание события углового"""
        return {
            "minute": minute,
            "type": "corner",
            "team_id": team["team_id"],
            "description": "Подача углового",
        }

    def _get_minute_intensity(self, minute: int) -> float:
        """Интенсивность игры по минутам"""
        if 1 <= minute <= 15:  # Начало тайма
            return 0.7
        elif 16 <= minute <= 30:  # Середина тайма
            return 0.5
        elif 31 <= minute <= 45:  # Конец тайма
            return 0.8
        elif 46 <= minute <= 60:  # Начало второго тайма
            return 0.6
        elif 61 <= minute <= 75:  # Середина второго тайма
            return 0.5
        else:  # Конец матча
            return 0.9

    def _get_minute_pressure(self, minute: int) -> float:
        """Давление по минутам (влияет на вероятность гола)"""
        if minute <= 15:
            return 0.8  # Начало - игроки не разыгрались
        elif minute <= 30:
            return 1.0  # Оптимальная форма
        elif minute <= 45:
            return 1.2  # Конец тайма - усталость вратаря
        elif minute <= 60:
            return 0.9  # Начало второго тайма
        elif minute <= 75:
            return 1.0  # Середина
        else:
            return 1.3  # Конец матча - решающие моменты

    def _calculate_score(
        self, events: List[Dict], home_team_id: int, away_team_id: int
    ) -> Dict:
        """Расчет счета на основе событий"""
        home_goals = len(
            [e for e in events if e["type"] == "goal" and e["team_id"] == home_team_id]
        )
        away_goals = len(
            [e for e in events if e["type"] == "goal" and e["team_id"] == away_team_id]
        )
        return {"home": home_goals, "away": away_goals}

    def _calculate_statistics(
        self, events: List[Dict], home_team_id: int, away_team_id: int
    ) -> Dict:
        """Расчет статистики матча"""
        home_shots = len(
            [e for e in events if e["type"] == "shot" and e["team_id"] == home_team_id]
        )
        away_shots = len(
            [e for e in events if e["type"] == "shot" and e["team_id"] == away_team_id]
        )

        home_shots_on_target = len(
            [
                e
                for e in events
                if e["type"] == "shot"
                and e["team_id"] == home_team_id
                and e.get("on_target")
            ]
        )
        away_shots_on_target = len(
            [
                e
                for e in events
                if e["type"] == "shot"
                and e["team_id"] == away_team_id
                and e.get("on_target")
            ]
        )

        home_fouls = len(
            [e for e in events if e["type"] == "foul" and e["team_id"] == home_team_id]
        )
        away_fouls = len(
            [e for e in events if e["type"] == "foul" and e["team_id"] == away_team_id]
        )

        home_corners = len(
            [
                e
                for e in events
                if e["type"] == "corner" and e["team_id"] == home_team_id
            ]
        )
        away_corners = len(
            [
                e
                for e in events
                if e["type"] == "corner" and e["team_id"] == away_team_id
            ]
        )

        home_yellow_cards = len(
            [
                e
                for e in events
                if e["type"] == "yellow_card" and e["team_id"] == home_team_id
            ]
        )
        away_yellow_cards = len(
            [
                e
                for e in events
                if e["type"] == "yellow_card" and e["team_id"] == away_team_id
            ]
        )

        # Владение мячом (примерное на основе событий)
        total_events = (
            home_shots
            + away_shots
            + home_fouls
            + away_fouls
            + home_corners
            + away_corners
        )
        if total_events > 0:
            home_possession = int(
                ((home_shots + home_fouls + home_corners) / total_events) * 100
            )
            away_possession = 100 - home_possession
        else:
            home_possession, away_possession = 50, 50

        return {
            "possession": {"home": home_possession, "away": away_possession},
            "shots": {"home": home_shots, "away": away_shots},
            "shots_on_target": {
                "home": home_shots_on_target,
                "away": away_shots_on_target,
            },
            "fouls": {"home": home_fouls, "away": away_fouls},
            "corners": {"home": home_corners, "away": away_corners},
            "yellow_cards": {"home": home_yellow_cards, "away": away_yellow_cards},
        }

    def _determine_winner(
        self, score: Dict, home_team_id: int, away_team_id: int
    ) -> int:
        """Определение победителя матча"""
        if score["home"] > score["away"]:
            return home_team_id
        elif score["home"] < score["away"]:
            return away_team_id
        else:
            # Ничья - можно добавить пенальти позже
            return None

    def _find_team(self, team_id: int) -> Dict:
        """Найти команду по ID"""
        return next((team for team in self.teams if team["team_id"] == team_id), None)


class LiveMatchSimulator(MatchSimulator):
    """Симулятор матча в реальном времени с пошаговым выводом"""

    def simulate_live_match(self, match: Dict, delay: float = 0.5):
        """Симуляция матча с пошаговым выводом"""
        print(f"\n🎥 Начинаем прямую трансляцию матча!")
        print(
            f"Команда {self._find_team(match['home_team_id'])['team_name']} vs {self._find_team(match['away_team_id'])['team_name']}"
        )
        print("=" * 50)

        events = []
        home_score = 0
        away_score = 0

        for minute in range(1, 91):
            time.sleep(delay)

            # Шанс события в эту минуту
            if random.random() < 0.3:
                event = self._simulate_minute_event(
                    match, minute, home_score, away_score
                )
                if event:
                    events.append(event)
                    self._display_live_event(event, home_score, away_score)

                    if event["type"] == "goal":
                        if event["team_id"] == match["home_team_id"]:
                            home_score += 1
                        else:
                            away_score += 1

        # Завершение матча
        print(f"\n🏁 МАТЧ ЗАВЕРШЕН!")
        print(f"ФИНАЛЬНЫЙ СЧЕТ: {home_score} - {away_score}")

        # Обновление данных матча
        match.update(
            {
                "status": "completed",
                "score": {"home": home_score, "away": away_score},
                "events": events,
                "statistics": self._calculate_statistics(
                    events, match["home_team_id"], match["away_team_id"]
                ),
                "winner_id": self._determine_winner(
                    {"home": home_score, "away": away_score},
                    match["home_team_id"],
                    match["away_team_id"],
                ),
            }
        )

        return match

    def _simulate_minute_event(
        self, match: Dict, minute: int, home_score: int, away_score: int
    ) -> Dict:
        """Симуляция события в конкретную минуту"""
        home_team = self._find_team(match["home_team_id"])
        away_team = self._find_team(match["away_team_id"])

        # Простая логика для демонстрации
        if random.random() < 0.1:  # 10% шанс гола
            if random.random() < 0.6:  # 60% шанс что домашние забивают
                return self._create_simple_goal_event(home_team, minute)
            else:
                return self._create_simple_goal_event(away_team, minute)
        elif random.random() < 0.15:  # 15% шанс другого события
            return self._create_simple_other_event(
                home_team if random.random() < 0.5 else away_team, minute
            )

        return None

    def _create_simple_goal_event(self, team: Dict, minute: int) -> Dict:
        """Создание простого события гола"""
        scorer = self._select_attacking_player(team)
        return {
            "minute": minute,
            "type": "goal",
            "team_id": team["team_id"],
            "player_id": scorer["id"] if scorer else None,
            "description": f"{scorer['name'] if scorer else 'Игрок'} забивает гол на {minute}-й минуте!",
        }

    def _create_simple_other_event(self, team: Dict, minute: int) -> Dict:
        """Создание простого другого события"""
        event_type = random.choice(["shot", "foul", "corner"])
        player = self._select_random_player(team)

        descriptions = {
            "shot": "Опасный момент! Удар по воротам!",
            "foul": "Нарушение правил!",
            "corner": "Подача углового",
        }

        return {
            "minute": minute,
            "type": event_type,
            "team_id": team["team_id"],
            "player_id": player["id"] if player else None,
            "description": f"{descriptions[event_type]} ({minute}')",
        }

    def _display_live_event(self, event: Dict, home_score: int, away_score: int):
        """Отображение события в реальном времени"""
        minute = event["minute"]

        if event["type"] == "goal":
            print(f"⚽ {minute}' ГОООЛ! {event['description']}")
            print(f"   Счет: {home_score}-{away_score}")
        elif event["type"] == "shot":
            print(f"🎯 {minute}' {event['description']}")
        elif event["type"] == "foul":
            print(f"💥 {minute}' {event['description']}")
        elif event["type"] == "corner":
            print(f"↩️ {minute}' {event['description']}")
