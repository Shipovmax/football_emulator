import random
import time
from typing import Any, Dict, List, Optional

from .calculators import MatchCalculator, ProbabilityCalculator


class MatchSimulator:
    def __init__(
        self, players: List[Dict[str, Any]], teams: List[Dict[str, Any]]
    ) -> None:
        self.players = players
        self.teams = teams
        self.calculator = MatchCalculator(players)
        self.prob_calculator = ProbabilityCalculator()

    def simulate_match(
        self, match: Dict[str, Any], seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """Run a full match simulation with dynamic event generation."""
        if seed is not None:
            random.seed(seed)

        home_team = self._find_team(match["home_team_id"])
        away_team = self._find_team(match["away_team_id"])

        if not home_team or not away_team:
            return match

        # Team power ratings used to weight event generation
        home_power = self.calculator.calculate_team_power(home_team)
        away_power = self.calculator.calculate_team_power(away_team)

        # Generate the minute-by-minute match events
        events = self._simulate_match_events(
            home_team, away_team, home_power, away_power
        )

        # Compute final score and aggregate statistics
        score = self._calculate_score(
            events, home_team["team_id"], away_team["team_id"]
        )
        statistics = self._calculate_statistics(
            events, home_team["team_id"], away_team["team_id"]
        )

        # Determine the winner
        winner_id = self._determine_winner(
            score, home_team["team_id"], away_team["team_id"]
        )

        # Persist results back onto the match record
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
        self,
        home_team: Dict[str, Any],
        away_team: Dict[str, Any],
        home_power: float,
        away_power: float,
    ) -> List[Dict[str, Any]]:
        """Simulate all match events minute by minute."""
        events = []
        home_score = 0
        away_score = 0

        # Power balance, factoring in home advantage
        home_advantage = 1.15
        total_power = home_power * home_advantage + away_power
        home_attack_prob = (home_power * home_advantage) / total_power
        away_attack_prob = away_power / total_power

        # Simulate minute by minute (1-90)
        for minute in range(1, 91):
            # Attack intensity depends on the current minute
            intensity = self._get_minute_intensity(minute)

            # Decide which team is attacking
            if random.random() < intensity:
                if random.random() < home_attack_prob:
                    # Home team attack
                    event = self._simulate_attack(home_team, away_team, minute, "home")
                    if event:
                        events.append(event)
                        if event["type"] == "goal":
                            home_score += 1
                else:
                    # Away team attack
                    event = self._simulate_attack(away_team, home_team, minute, "away")
                    if event:
                        events.append(event)
                        if event["type"] == "goal":
                            away_score += 1

            # Chance of a non-attack event (foul, card)
            if random.random() < 0.1:
                event = self._simulate_non_attack_event(
                    home_team, away_team, minute, home_attack_prob
                )
                if event:
                    events.append(event)

        return sorted(events, key=lambda x: x["minute"])

    def _simulate_attack(
        self,
        attacking_team: Dict[str, Any],
        defending_team: Dict[str, Any],
        minute: int,
        side: str,
    ) -> Optional[Dict[str, Any]]:
        """Simulate a single attacking possession."""
        # Pick the attacking player
        attacker = self._select_attacking_player(attacking_team)
        if not attacker:
            return None

        # Pick the defender and goalkeeper
        defender = self._select_defending_player(defending_team)
        goalkeeper = self._select_goalkeeper(defending_team)

        if not goalkeeper:
            return None

        # Compute goal probability
        goal_probability = self.prob_calculator.calculate_goal_probability(
            attacker, defender, goalkeeper
        )

        # Apply minute-based modifier
        minute_modifier = self._get_minute_pressure(minute)
        final_probability = goal_probability * minute_modifier

        # Resolve the outcome of the attack
        if random.random() < final_probability:
            # GOAL!
            return self._create_goal_event(
                attacking_team, defending_team, attacker, minute, side
            )
        elif random.random() < 0.3:
            # Shot off target / blocked
            return self._create_shot_event(
                attacking_team, attacker, minute, side, on_target=False
            )
        elif random.random() < 0.4:
            # Shot on target (saved)
            return self._create_shot_event(
                attacking_team, attacker, minute, side, on_target=True
            )
        elif random.random() < 0.2:
            # Foul during the attack
            return self._create_foul_event(defending_team, minute, side)

        return None

    def _simulate_non_attack_event(
        self,
        home_team: Dict[str, Any],
        away_team: Dict[str, Any],
        minute: int,
        home_attack_prob: float,
    ) -> Optional[Dict[str, Any]]:
        """Simulate a non-attack event (foul, corner, etc.)."""
        event_type = random.choices(
            ["foul", "corner", "yellow_card", "offside"], weights=[0.5, 0.3, 0.15, 0.05]
        )[0]

        # Pick which team the event belongs to
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
                "description": "Yellow card for rough play",
            }
        elif event_type == "offside":
            return {
                "minute": minute,
                "type": "offside",
                "team_id": team["team_id"],
                "description": "Offside",
            }

        return None

    def _select_attacking_player(
        self, team: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Pick an attacking player, prioritized by position."""
        positions = ["forward", "winger", "attacking_midfielder", "center_midfielder"]
        for position in positions:
            players = [
                p
                for p in self.players
                if p["id"] in team["player_ids"] and p["position"] == position
            ]
            if players:
                # Weight the selection by attack rating
                weights = [p["attack"] for p in players]
                return random.choices(players, weights=weights)[0]
        return self._select_random_player(team)

    def _select_defending_player(
        self, team: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Pick a defending player, prioritized by position."""
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

    def _select_goalkeeper(self, team: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Pick the team's goalkeeper."""
        goalkeepers = [
            p
            for p in self.players
            if p["id"] in team["player_ids"] and p["position"] == "goalkeeper"
        ]
        return random.choice(goalkeepers) if goalkeepers else None

    def _select_random_player(self, team: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Pick a random player from the team."""
        team_players = [p for p in self.players if p["id"] in team["player_ids"]]
        return random.choice(team_players) if team_players else None

    def _create_goal_event(
        self,
        attacking_team: Dict[str, Any],
        defending_team: Dict[str, Any],
        scorer: Dict[str, Any],
        minute: int,
        side: str,
    ) -> Dict[str, Any]:
        """Build a goal event."""
        goal_types = ["open_play", "header", "long_shot", "penalty", "free_kick"]
        goal_type = random.choices(goal_types, weights=[0.6, 0.15, 0.15, 0.05, 0.05])[0]

        # Possible assist
        assister = None
        if random.random() < 0.7:  # 70% of goals include an assist
            assister = self._select_attacking_player(attacking_team)
            while assister and assister["id"] == scorer["id"]:
                assister = self._select_attacking_player(attacking_team)

        descriptions = {
            "open_play": [
                "A beautiful strike from outside the box!",
                "Coolly beat the goalkeeper!",
                "Powerful shot into the near corner!",
                "A precise low shot!",
            ],
            "header": [
                "A magnificent header!",
                "Rose to meet the cross and finished it!",
                "A powerful header from beyond the goalkeeper's reach!",
            ],
            "long_shot": [
                "An incredible goal from distance!",
                "Shoots from afar... GOAL!",
                "A powerful strike from outside the box!",
            ],
            "penalty": [
                "A perfectly placed penalty!",
                "Coolly converted the penalty!",
                "The goalkeeper guessed right but couldn't reach it!",
            ],
            "free_kick": [
                "A magnificent free kick goal!",
                "Shoots... off the post... GOAL!",
                "An unstoppable free kick!",
            ],
        }

        description = random.choice(descriptions[goal_type])
        if assister:
            description = (
                f"{assister['name']} passes to {scorer['name']}. {description}"
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
        self,
        team: Dict[str, Any],
        shooter: Dict[str, Any],
        minute: int,
        side: str,
        on_target: bool,
    ) -> Dict[str, Any]:
        """Build a shot event."""
        descriptions_on = [
            "A powerful shot on target!",
            "Dangerous moment! Shot at goal!",
            "Trying a strike from outside the box!",
        ]
        descriptions_off = [
            "Shot wide of the goal!",
            "Fires over the crossbar!",
            "Missed the target!",
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

    def _create_foul_event(
        self, team: Dict[str, Any], minute: int, side: str
    ) -> Dict[str, Any]:
        """Build a foul event."""
        fouler = self._select_random_player(team)
        descriptions = ["A hard tackle!", "A foul!", "Rough play!"]

        # Chance of a card
        card = None
        if random.random() < 0.3:
            card = "yellow" if random.random() < 0.9 else "red"

        card_text = (
            "a yellow card"
            if card == "yellow"
            else "a red card" if card == "red" else "a warning"
        )
        return {
            "minute": minute,
            "type": "foul",
            "team_id": team["team_id"],
            "player_id": fouler["id"] if fouler else None,
            "card": card,
            "description": f"{random.choice(descriptions)} {fouler['name'] if fouler else 'The player'} receives {card_text}.",
        }

    def _create_corner_event(
        self, team: Dict[str, Any], minute: int, side: str
    ) -> Dict[str, Any]:
        """Build a corner-kick event."""
        return {
            "minute": minute,
            "type": "corner",
            "team_id": team["team_id"],
            "description": "Corner kick",
        }

    def _get_minute_intensity(self, minute: int) -> float:
        """Return the probability of an attack occurring in a given minute."""
        if 1 <= minute <= 15:  # Start of first half
            return 0.7
        elif 16 <= minute <= 30:  # Mid first half
            return 0.5
        elif 31 <= minute <= 45:  # End of first half
            return 0.8
        elif 46 <= minute <= 60:  # Start of second half
            return 0.6
        elif 61 <= minute <= 75:  # Mid second half
            return 0.5
        else:  # End of match
            return 0.9

    def _get_minute_pressure(self, minute: int) -> float:
        """Return the goal-probability modifier for a given minute."""
        if minute <= 15:
            return 0.8  # Start - players not yet warmed up
        elif minute <= 30:
            return 1.0  # Peak form
        elif minute <= 45:
            return 1.2  # End of first half - goalkeeper fatigue
        elif minute <= 60:
            return 0.9  # Start of second half
        elif minute <= 75:
            return 1.0  # Midway
        else:
            return 1.3  # End of match - decisive moments

    def _calculate_score(
        self, events: List[Dict[str, Any]], home_team_id: int, away_team_id: int
    ) -> Dict[str, int]:
        """Compute the final score from the event list."""
        home_goals = len(
            [e for e in events if e["type"] == "goal" and e["team_id"] == home_team_id]
        )
        away_goals = len(
            [e for e in events if e["type"] == "goal" and e["team_id"] == away_team_id]
        )
        return {"home": home_goals, "away": away_goals}

    def _calculate_statistics(
        self, events: List[Dict[str, Any]], home_team_id: int, away_team_id: int
    ) -> Dict[str, Any]:
        """Aggregate match statistics from the event list."""
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

        # Approximate possession, derived from the event mix
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
        self, score: Dict[str, int], home_team_id: int, away_team_id: int
    ) -> Optional[int]:
        """Determine the winning team ID, or None for a draw."""
        if score["home"] > score["away"]:
            return home_team_id
        elif score["home"] < score["away"]:
            return away_team_id
        else:
            # Draw - penalty shootout could be added later
            return None

    def _find_team(self, team_id: int) -> Optional[Dict[str, Any]]:
        """Find a team by ID."""
        return next((team for team in self.teams if team["team_id"] == team_id), None)


class LiveMatchSimulator(MatchSimulator):
    """Real-time match simulator with step-by-step output."""

    def simulate_live_match(
        self, match: Dict[str, Any], delay: float = 0.5
    ) -> Dict[str, Any]:
        """Simulate a match with a step-by-step live feed."""
        print("\n🎥 Starting the live match broadcast!")
        print(
            f"{self._find_team(match['home_team_id'])['team_name']} vs {self._find_team(match['away_team_id'])['team_name']}"
        )
        print("=" * 50)

        events = []
        home_score = 0
        away_score = 0

        for minute in range(1, 91):
            time.sleep(delay)

            # Chance of an event occurring this minute
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

        # Match complete
        print("\n🏁 MATCH FINISHED!")
        print(f"FINAL SCORE: {home_score} - {away_score}")

        # Persist results back onto the match record
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
        self, match: Dict[str, Any], minute: int, home_score: int, away_score: int
    ) -> Optional[Dict[str, Any]]:
        """Simulate an event for a specific minute."""
        home_team = self._find_team(match["home_team_id"])
        away_team = self._find_team(match["away_team_id"])

        # Simplified logic for the live-feed demo
        if random.random() < 0.1:  # 10% chance of a goal
            if random.random() < 0.6:  # 60% chance the home team scores
                return self._create_simple_goal_event(home_team, minute)
            else:
                return self._create_simple_goal_event(away_team, minute)
        elif random.random() < 0.15:  # 15% chance of another event
            return self._create_simple_other_event(
                home_team if random.random() < 0.5 else away_team, minute
            )

        return None

    def _create_simple_goal_event(
        self, team: Dict[str, Any], minute: int
    ) -> Dict[str, Any]:
        """Build a simplified goal event for the live feed."""
        scorer = self._select_attacking_player(team)
        return {
            "minute": minute,
            "type": "goal",
            "team_id": team["team_id"],
            "player_id": scorer["id"] if scorer else None,
            "description": f"{scorer['name'] if scorer else 'A player'} scores in the {minute}th minute!",
        }

    def _create_simple_other_event(
        self, team: Dict[str, Any], minute: int
    ) -> Dict[str, Any]:
        """Build a simplified non-goal event for the live feed."""
        event_type = random.choice(["shot", "foul", "corner"])
        player = self._select_random_player(team)

        descriptions = {
            "shot": "Dangerous moment! Shot at goal!",
            "foul": "A foul!",
            "corner": "Corner kick",
        }

        return {
            "minute": minute,
            "type": event_type,
            "team_id": team["team_id"],
            "player_id": player["id"] if player else None,
            "description": f"{descriptions[event_type]} ({minute}')",
        }

    def _display_live_event(
        self, event: Dict[str, Any], home_score: int, away_score: int
    ) -> None:
        """Print a live event to the console."""
        minute = event["minute"]

        if event["type"] == "goal":
            print(f"⚽ {minute}' GOAL! {event['description']}")
            print(f"   Score: {home_score}-{away_score}")
        elif event["type"] == "shot":
            print(f"🎯 {minute}' {event['description']}")
        elif event["type"] == "foul":
            print(f"💥 {minute}' {event['description']}")
        elif event["type"] == "corner":
            print(f"↩️ {minute}' {event['description']}")
