import random

import matplotlib.pyplot as plt


class MontyHallSimulator:
    def __init__(self, num_games=1000, num_doors=3, switch_strategy=None):
        """
        Initialize the Monty Hall game simulator.

        Parameters:
        - num_games (int): Number of Monty Hall games to simulate. Default is 1000.
        - num_doors (int): Number of doors in each game. Default is 3.
        - switch_strategy (bool): Whether to always switch doors. 
                                  If None, it's chosen randomly for each game. Default is None.
        """
        self.num_games = num_games
        self.num_doors = num_doors
        self.switch_strategy = switch_strategy
        self.results = {
            'win_changed': 0,
            'win_unchanged': 0,
            'lose_changed': 0,
            'lose_unchanged': 0,
            'win_percentage': {'changed': [], 'unchanged': []},
        }

    def play_game(self):
        """
        Simulate a single Monty Hall game.

        Returns:
        - bool: True if the player wins, False otherwise.
        """
        doors = list(range(1, self.num_doors + 1))
        winning_door = random.choice(doors)
        player_choice = random.choice(doors)

        # Host reveals a door with a goat, which is not the chosen or the winning door
        remaining_doors = [door for door in doors 
                           if door != player_choice and door != winning_door]
        host_reveal = random.choice(remaining_doors)

        # Determine if the player switches doors or not
        if self.switch_strategy is None:
            switch = random.choice([True, False])
        else:
            switch = self.switch_strategy

        # If switching, player switches to the remaining unopened door
        if switch:
            player_choice = [door for door in doors 
                             if door != player_choice and door != host_reveal][0]

        # Update game results
        if player_choice == winning_door:
            result = 'win'
        else:
            result = 'lose'

        if switch:
            result += '_changed'
        else:
            result += '_unchanged'

        self.results[result] += 1

    def simulate_games(self):
        """
        Simulate multiple Monty Hall games and collect statistics.
        """
        for _ in range(self.num_games):
            self.play_game()
            
            # Calculate win percentages for both strategies
            total_changed = self.results['win_changed'] + self.results['lose_changed']
            total_unchanged = self.results['win_unchanged'] + self.results['lose_unchanged']
            
            if total_changed > 0:
                win_changed_percentage = self.results['win_changed'] / total_changed
                self.results['win_percentage']['changed'].append(win_changed_percentage)

            if total_unchanged > 0:
                win_unchanged_percentage = self.results['win_unchanged'] / total_unchanged
                self.results['win_percentage']['unchanged'].append(win_unchanged_percentage)

    def plot_results(self):
        """
        Plot the win percentages for switching and not switching doors.
        """
        plt.figure(figsize=(12, 6))
        
        # Plot for the switching case
        if len(self.results['win_percentage']['changed']) > 0:
            x_values_changed = range(1, len(self.results['win_percentage']['changed']) + 1)
            plt.plot(x_values_changed, self.results['win_percentage']['changed'], 
                     label='Switch Doors')
        
        # Plot for the unchanged case
        if len(self.results['win_percentage']['unchanged']) > 0:
            x_values_unchanged = range(1, len(self.results['win_percentage']['unchanged']) + 1)
            plt.plot(x_values_unchanged, self.results['win_percentage']['unchanged'], 
                     label='Stay with Initial Choice')
        
        plt.title(f'Monty Hall Simulation ({self.num_games} Games)', fontsize=18)
        plt.xlabel('Game Number', fontsize=16)
        plt.ylabel('Win Probability', fontsize=16)
        plt.legend(fontsize=14)
        plt.show()


if __name__ == "__main__":
    num_games_to_simulate = 1000

    # Simulate with always switching doors
    simulator_switch = MontyHallSimulator(num_games=num_games_to_simulate, switch_strategy=True)
    simulator_switch.simulate_games()

    # Simulate without switching doors
    simulator_no_switch = MontyHallSimulator(num_games=num_games_to_simulate, switch_strategy=False)
    simulator_no_switch.simulate_games()

    # Plot the results
    simulator_switch.plot_results()
    simulator_no_switch.plot_results()
