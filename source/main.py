"""
Main entry point for the football emulator, with a menu-driven navigation flow.
"""

import os
import sys
import time
from typing import Any, Dict, Optional

# Add module search paths relative to this file
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

# Color codes shared across the console UI
GREEN_COLOR = "\033[92m"
BLUE_COLOR = "\033[94m"
YELLOW_COLOR = "\033[93m"
RED_COLOR = "\033[91m"
CYAN_COLOR = "\033[96m"
RESET_COLOR = "\033[0m"


class AdvancedFootballEmulator:
    def __init__(self) -> None:
        self.players, self.teams, self.matches = load_all_data()
        self.simulator = MatchSimulator(self.players, self.teams)
        self.current_state = "main_menu"
        self.selected_match: Optional[Dict[str, Any]] = None
        self.selected_team: Optional[Dict[str, Any]] = None
        self.selected_player: Optional[Dict[str, Any]] = None

    def run(self) -> None:
        """Run the emulator's main event loop."""
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
                print("\n\n🔚 Exiting the program...")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                self.current_state = "main_menu"

    def show_main_menu(self) -> None:
        """Display the main menu."""
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
            print("👋 Goodbye!")
            sys.exit()
        else:
            print("❌ Invalid choice. Try again.")

    def show_tournament_bracket(self) -> None:
        """Display the tournament bracket."""
        print_tournament_bracket(self.matches, self.teams)
        print_secondary_menu("main menu")
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
                print("❌ Match not found!")
        else:
            print("❌ Invalid choice!")

    def show_match_details(self) -> None:
        """Display the details of the selected match."""
        if not self.selected_match:
            self.current_state = "tournament_bracket"
            return

        print_match_details(self.selected_match, self.teams, self.players)

        print(f"\n{YELLOW_COLOR}ADDITIONAL OPTIONS:{RESET_COLOR}")
        print("1 - 🔄 Simulate match (if not played)")
        print("2 - 👥 Show team lineups")
        print("3 - 📊 Detailed statistics")
        print("0 - ↩️ Back to bracket")
        print("\nChoose an option: ", end="")

        choice = input().strip()

        if choice == "1" and self.selected_match["status"] != "completed":
            # Use the current time as the random seed
            seed = int(time.time())
            self.simulator.simulate_match(self.selected_match, seed=seed)
            print("✅ Match simulated successfully!")
        elif choice == "2":
            self.show_match_lineups()
        elif choice == "3":
            self.show_detailed_stats()
        elif choice == "0":
            self.current_state = "tournament_bracket"
            self.selected_match = None
        else:
            print("❌ Invalid choice!")

    def show_match_lineups(self) -> None:
        """Display both teams' lineups for the selected match."""
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

        print(f"\n{CYAN_COLOR}=== TEAM LINEUPS ==={RESET_COLOR}")

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
            f"\n{YELLOW_COLOR}Select a player by ID to view their card or 0 to go back: {RESET_COLOR}",
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
                print("❌ Player not found!")

    def show_teams_list(self) -> None:
        """Display the full list of teams."""
        print_teams_table(self.teams, self.players)

        print(
            f"\n{YELLOW_COLOR}Select a team by ID for details or 0 to go back: {RESET_COLOR}",
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
                print("❌ Team not found!")
        else:
            print("❌ Invalid choice!")

    def show_team_details(self) -> None:
        """Display the details of the selected team."""
        if not self.selected_team:
            self.current_state = "teams_list"
            return

        team_players = [
            p for p in self.players if p["id"] in self.selected_team["player_ids"]
        ]
        print_team_card(self.selected_team, team_players)
        print_players_table(team_players, self.selected_team["team_name"])

        print(
            f"\n{YELLOW_COLOR}Select a player by ID to view their card or 0 to go back: {RESET_COLOR}",
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
                print("❌ Player not found!")
        else:
            print("❌ Invalid choice!")

    def show_players_list(self) -> None:
        """Display the full list of players."""
        print_players_table(self.players)

        print(
            f"\n{YELLOW_COLOR}Select a player by ID to view their card or 0 to go back: {RESET_COLOR}",
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
                print("❌ Player not found!")
        else:
            print("❌ Invalid choice!")

    def show_player_details(self) -> None:
        """Display the selected player's card."""
        if not self.selected_player:
            self.current_state = "players_list"
            return

        print_player_card_ascii(self.selected_player)

        print(f"\n{YELLOW_COLOR}ADDITIONAL OPTIONS:{RESET_COLOR}")
        print("1 - 🔄 Compare with another player")
        print("0 - ↩️ Back")
        print("\nChoose an option: ", end="")

        choice = input().strip()

        if choice == "1":
            self.compare_players()
        elif choice == "0":
            # Return to the previous state
            if self.selected_team:
                self.current_state = "team_details"
            else:
                self.current_state = "players_list"
            self.selected_player = None
        else:
            print("❌ Invalid choice!")

    def compare_players(self) -> None:
        """Compare the selected player against another player by ID."""
        print(
            f"\n{YELLOW_COLOR}Enter the ID of the second player to compare: {RESET_COLOR}",
            end="",
        )
        choice = input().strip()

        if choice.isdigit():
            player2_id = int(choice)
            player2 = next((p for p in self.players if p["id"] == player2_id), None)
            if player2:
                print_player_comparison(self.selected_player, player2)
                input(f"\n{YELLOW_COLOR}Press Enter to continue...{RESET_COLOR}")
            else:
                print("❌ Player not found!")
        else:
            print("❌ Invalid ID format!")

    def simulate_match(self) -> None:
        """Simulate a match chosen from the bracket."""
        print(f"\n{CYAN_COLOR}=== MATCH SIMULATION ==={RESET_COLOR}")
        print_tournament_bracket(self.matches, self.teams)

        print(
            f"\n{YELLOW_COLOR}Select a match to simulate (1-{len(self.matches)}) or 0 to cancel: {RESET_COLOR}",
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
                        "❌ This match has already been played! Simulate again? (y/n): ", end=""
                    )
                    if input().strip().lower() != "y":
                        return

                print("🔄 Simulating the match...")

                # Use the current time as the random seed
                seed = int(time.time())

                # Run the dynamic simulation
                self.simulator.simulate_match(match, seed=seed)
                print("✅ Match simulated successfully!")
                self.selected_match = match
                self.current_state = "match_details"
            else:
                print("❌ Match not found!")
        else:
            print("❌ Invalid choice!")

    def show_advanced_stats(self) -> None:
        """Display advanced player and team statistics."""
        print(f"\n{CYAN_COLOR}=== ADVANCED STATISTICS ==={RESET_COLOR}")

        # Top players by overall rating
        top_players = sorted(self.players, key=lambda x: x["overall"], reverse=True)[:5]
        print(f"\n{YELLOW_COLOR}🏆 TOP 5 PLAYERS BY RATING:{RESET_COLOR}")
        for i, player in enumerate(top_players, 1):
            print(f"{i}. {player['name']} - {player['overall']} OVR")

        # Team statistics
        print(f"\n{YELLOW_COLOR}📈 TEAM STATISTICS:{RESET_COLOR}")
        for team in self.teams:
            team_players = [p for p in self.players if p["id"] in team["player_ids"]]
            avg_age = sum(p["age"] for p in team_players) / len(team_players)
            avg_rating = sum(p["overall"] for p in team_players) / len(team_players)
            print(
                f"{team['team_name']}: average age {avg_age:.1f}, average rating {avg_rating:.1f}"
            )

        input(f"\n{YELLOW_COLOR}Press Enter to go back...{RESET_COLOR}")

    def show_detailed_stats(self) -> None:
        """Display detailed statistics for the selected match."""
        if not self.selected_match or not self.selected_match.get("statistics"):
            print("❌ No statistics available for this match!")
            return

        stats = self.selected_match["statistics"]
        print(f"\n{CYAN_COLOR}=== DETAILED MATCH ANALYTICS ==={RESET_COLOR}")

        # Attack efficiency analysis
        home_shots = stats["shots"]["home"]
        home_on_target = stats["shots_on_target"]["home"]
        home_efficiency = (home_on_target / home_shots * 100) if home_shots > 0 else 0

        away_shots = stats["shots"]["away"]
        away_on_target = stats["shots_on_target"]["away"]
        away_efficiency = (away_on_target / away_shots * 100) if away_shots > 0 else 0

        print(f"\n{YELLOW_COLOR}🎯 ATTACK EFFICIENCY:{RESET_COLOR}")
        print(
            f"Home team: {home_efficiency:.1f}% ({home_on_target}/{home_shots} on target)"
        )
        print(
            f"Away team: {away_efficiency:.1f}% ({away_on_target}/{away_shots} on target)"
        )

        input(f"\n{YELLOW_COLOR}Press Enter to go back...{RESET_COLOR}")


def main() -> None:
    """Application entry point."""
    try:
        print("🚀 Starting the football emulator...")
        emulator = AdvancedFootballEmulator()
        emulator.run()
    except KeyboardInterrupt:
        print("\n\n🔚 Program interrupted by user")
    except Exception as e:
        print(f"\n💥 Critical error: {e}")


if __name__ == "__main__":
    main()
