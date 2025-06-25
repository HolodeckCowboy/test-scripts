import random
from collections import defaultdict


class SlotGameSimulator:
    def __init__(self, reels, symbols):
        """
        Initialize the slot game simulator.

        Args:
            reels (list of lists): The reels configuration (m rows x n columns)
            symbols (list): List of possible symbols in the game (0-13)
        """
        self.reels = reels
        self.symbols = symbols
        self.rows = 3  # We always display 3 rows
        self.cols = len(reels)
        self.WILD = 0  # Define which symbol is the wild/joker
        self.PREMIUM_SYMBOLS = {12, 13}  # Symbols that require pure sequences

        # Validate reels
        for i, reel in enumerate(reels):
            if len(reel) < self.rows:
                raise ValueError(f"Reel {i} is too short (length {len(reel)}), needs at least {self.rows} symbols")

    def spin(self):
        """
        Simulate a single spin of the slot game.

        Returns:
            tuple: (result_grid, prizes)
                   result_grid: 3x5 grid of symbols
                   prizes: list of prize dictionaries {symbol: x, amount: y}
        """
        # Choose random stop positions for each reel
        stop_positions = [random.randint(0, len(reel) - 1) for reel in self.reels]

        # Build the result grid (3 rows x 5 columns)
        result_grid = []
        for row in range(self.rows):
            result_row = []
            for col in range(self.cols):
                reel = self.reels[col]
                pos = (stop_positions[col] + row) % len(reel)
                result_row.append(reel[pos])
            result_grid.append(result_row)

        # Find all winning combinations
        prizes = self._calculate_prizes(result_grid)

        return result_grid, prizes

    def _calculate_prizes(self, grid):
        """
        Calculate prizes from the result grid with wild symbol (0) support.
        Premium symbols (12,13) only form wins in pure sequences (no wilds).
        """
        prizes = []

        # Check each row
        for row in grid:
            # Find all possible sequences in this row
            row_prizes = self._find_sequences(row)
            if row_prizes:
                prizes.extend(row_prizes)

        # Only keep the highest prize for each symbol
        max_prizes = {}
        for prize in prizes:
            symbol = prize['symbol']
            if symbol not in max_prizes or prize['amount'] > max_prizes[symbol]['amount']:
                max_prizes[symbol] = prize

        return list(max_prizes.values())

    def _find_sequences(self, symbols):
        """
        Find all winning sequences in a list of symbols, with special handling for:
        - Wilds (0) can substitute for any symbol except premium symbols (12,13)
        - Premium symbols only form wins in pure sequences (no wilds)
        """
        sequences = {}
        current_symbol = None
        current_count = 0
        wild_count = 0

        for i, symbol in enumerate(symbols):
            # Handle wild symbol
            if symbol == self.WILD:
                wild_count += 1
                if current_symbol is not None and current_symbol not in self.PREMIUM_SYMBOLS:
                    current_count += 1
                continue

            # Handle premium symbols (require pure sequences)
            if symbol in self.PREMIUM_SYMBOLS:
                # Reset if we were in a different sequence
                if current_symbol != symbol:
                    if current_count >= 3 and current_symbol is not None:
                        self._update_sequences(sequences, current_symbol, current_count)
                    current_symbol = symbol
                    current_count = 1
                    wild_count = 0
                else:
                    current_count += 1
                continue

            # Handle regular symbols
            if current_symbol == symbol:
                current_count += 1
            else:
                # Reset if we were in a different sequence
                if current_count >= 3 and current_symbol is not None:
                    self._update_sequences(sequences, current_symbol, current_count)

                # Start new sequence with any leading wilds
                current_symbol = symbol
                current_count = 1 + wild_count
                wild_count = 0

        # Check final sequence
        if current_count >= 3 and current_symbol is not None:
            self._update_sequences(sequences, current_symbol, current_count)

        # Convert to prize format
        return [{"symbol": sym, "amount": cnt} for sym, cnt in sequences.items()]

    def _update_sequences(self, sequences, symbol, count):
        """Update sequences dictionary with the best count for each symbol"""
        if symbol not in sequences or count > sequences[symbol]:
            sequences[symbol] = count

    def run_simulation(self, num_spins):
        """
        Run multiple simulations and collect statistics.
        """
        stats = {
            'total_spins': 0,
            'total_prizes': 0,
            'prize_combinations': defaultdict(int),  # Count of each prize combination (amount, symbol)
            'amount_counts': defaultdict(int),  # Count of each prize amount (3, 4, 5)
            'symbol_counts': defaultdict(int)  # Count of prizes per symbol
        }

        for _ in range(num_spins):
            print('iteration', _)
            _, prizes = self.spin()
            stats['total_spins'] += 1

            if prizes:
                stats['total_prizes'] += len(prizes)

                for prize in prizes:
                    # Track combination of amount and symbol
                    combo = (prize['amount'], prize['symbol'])
                    stats['prize_combinations'][combo] += 1
                    # Track individual counts
                    stats['amount_counts'][prize['amount']] += 1
                    stats['symbol_counts'][prize['symbol']] += 1

        return stats


# Example usage
if __name__ == "__main__":
    # Example reels configuration (5 reels, each with 10 symbols)
    # In a real game, these would be much longer and carefully balanced
    reels = [
          [
            6,
            6,
            3,
            11,
            11,
            11,
            8,
            5,
            8,
            9,
            7,
            8,
            10,
            8,
            11,
            8,
            8,
            7,
            6,
            13,
            13,
            11,
            6,
            3,
            11,
            10,
            10,
            7,
            8,
            9,
            3,
            12,
            7,
            11,
            12,
            6,
            8,
            9,
            7,
            7,
            11,
            10,
            9,
            13,
            11,
            13,
            3,
            13,
            9,
            9,
            8,
            10,
            6,
            5,
            8,
            10,
            11,
            6,
            3,
            11,
            5,
            7,
            8,
            11,
            9,
            10,
            7,
            5,
            11,
            11,
            6,
            10,
            6,
            9,
            9,
            11,
            1,
            8,
            5,
            11,
            11,
            7,
            4,
            9,
            1,
            9,
            1,
            12,
            11,
            10,
            9,
            4,
            6,
            5,
            10,
            1,
            7,
            13,
            13,
            9,
            2,
            13,
            3,
            1,
            2,
            4,
            11,
            6,
            7,
            6,
            2,
            4,
            4,
            2,
            11,
            3,
            5,
            8,
            11,
            5,
            6,
            6,
            3
          ],
          [
            10,
            6,
            8,
            0,
            11,
            5,
            0,
            11,
            5,
            11,
            3,
            5,
            1,
            5,
            10,
            1,
            10,
            7,
            10,
            13,
            13,
            9,
            10,
            10,
            7,
            5,
            4,
            4,
            5,
            1,
            5,
            12,
            9,
            9,
            12,
            7,
            11,
            9,
            5,
            9,
            9,
            6,
            7,
            13,
            11,
            13,
            4,
            13,
            10,
            7,
            7,
            0,
            9,
            11,
            11,
            11,
            9,
            10,
            10,
            12,
            7,
            9,
            6,
            6,
            5,
            7,
            8,
            0,
            11,
            6,
            3,
            9,
            0,
            5,
            8,
            6,
            7,
            5,
            9,
            8,
            6,
            7,
            11,
            0,
            7,
            9,
            7,
            12,
            5,
            3,
            8,
            7,
            0,
            9,
            9,
            6,
            11,
            13,
            13,
            4,
            11,
            13,
            8,
            2,
            5,
            1,
            3,
            10,
            0,
            11,
            1,
            6,
            3,
            8,
            11,
            9,
            0,
            1,
            9,
            2,
            10,
            6,
            8
          ],
          [
            9,
            5,
            4,
            0,
            9,
            8,
            0,
            11,
            11,
            7,
            4,
            5,
            1,
            10,
            10,
            1,
            10,
            4,
            10,
            13,
            13,
            6,
            4,
            3,
            9,
            9,
            4,
            8,
            10,
            1,
            5,
            12,
            6,
            4,
            12,
            7,
            9,
            9,
            11,
            10,
            6,
            7,
            7,
            13,
            4,
            13,
            6,
            13,
            8,
            7,
            6,
            0,
            11,
            8,
            7,
            4,
            6,
            4,
            3,
            12,
            7,
            6,
            11,
            11,
            9,
            3,
            9,
            0,
            5,
            8,
            10,
            10,
            0,
            2,
            2,
            8,
            5,
            7,
            6,
            8,
            7,
            4,
            6,
            0,
            5,
            2,
            11,
            12,
            3,
            11,
            2,
            2,
            0,
            10,
            3,
            7,
            13,
            6,
            13,
            7,
            8,
            13,
            5,
            1,
            8,
            3,
            6,
            6,
            0,
            6,
            6,
            12,
            3,
            5,
            7,
            8,
            1,
            9,
            8,
            1,
            9,
            5,
            4
          ],
          [
            6,
            4,
            6,
            0,
            4,
            11,
            5,
            10,
            7,
            8,
            5,
            4,
            1,
            8,
            10,
            1,
            11,
            6,
            7,
            13,
            13,
            11,
            10,
            7,
            4,
            5,
            7,
            6,
            9,
            1,
            1,
            12,
            6,
            3,
            12,
            3,
            8,
            4,
            3,
            9,
            11,
            11,
            3,
            13,
            4,
            13,
            6,
            13,
            7,
            7,
            11,
            1,
            10,
            8,
            8,
            4,
            11,
            10,
            7,
            12,
            11,
            8,
            9,
            9,
            6,
            4,
            10,
            1,
            8,
            5,
            6,
            3,
            0,
            6,
            5,
            10,
            11,
            5,
            6,
            10,
            3,
            3,
            2,
            0,
            11,
            4,
            8,
            12,
            3,
            1,
            5,
            6,
            0,
            4,
            4,
            8,
            4,
            13,
            13,
            5,
            5,
            13,
            2,
            7,
            8,
            7,
            5,
            7,
            0,
            4,
            10,
            12,
            3,
            10,
            7,
            6,
            1,
            7,
            7,
            10,
            6,
            4,
            6
          ],
          [
            3,
            9,
            3,
            10,
            2,
            3,
            7,
            3,
            6,
            12,
            11,
            7,
            5,
            8,
            11,
            3,
            3,
            10,
            10,
            13,
            13,
            10,
            8,
            11,
            4,
            9,
            8,
            2,
            3,
            9,
            8,
            12,
            6,
            5,
            12,
            8,
            11,
            6,
            4,
            8,
            10,
            4,
            6,
            13,
            4,
            13,
            9,
            13,
            11,
            9,
            3,
            8,
            5,
            2,
            9,
            3,
            10,
            8,
            11,
            12,
            7,
            11,
            4,
            7,
            1,
            11,
            8,
            5,
            5,
            9,
            11,
            10,
            11,
            9,
            4,
            10,
            2,
            1,
            1,
            3,
            7,
            10,
            1,
            5,
            2,
            11,
            2,
            12,
            2,
            5,
            4,
            10,
            6,
            8,
            6,
            2,
            2,
            13,
            13,
            7,
            6,
            13,
            2,
            12,
            10,
            4,
            10,
            7,
            6,
            10,
            7,
            12,
            1,
            5,
            1,
            1,
            8,
            3,
            9,
            11,
            3,
            9,
            3
          ]
        ]

    symbols = list(range(14))

    # Create simulator
    simulator = SlotGameSimulator(reels, symbols)

    # Run simulation
    num_spins = 100000000
    stats = simulator.run_simulation(num_spins)

    # Print results
    print(f"Simulation Results ({num_spins} spins):")
    print(f"Total games played: {stats['total_spins']}")
    print(f"Total prizes won: {stats['total_prizes']}")

    # Print prize combinations grouped by amount and symbol
    print("\nPrize combinations (amount-of-a-kind symbol: count):")

    # Get all unique amounts and sort them
    amounts = sorted({amt for amt, _ in stats['prize_combinations'].keys()})

    for amount in amounts:
        # Get all symbols that had this amount, sorted
        symbols_for_amount = sorted({sym for amt, sym in stats['prize_combinations'].keys() if amt == amount})

        for symbol in symbols_for_amount:
            count = stats['prize_combinations'].get((amount, symbol), 0)
            if count > 0:
                symbol_name = f"WILD" if symbol == 0 else str(symbol)
                print(f"  {amount}-of-a-kind {symbol_name}: {count} prizes")

    # Print summary statistics
    print("\nSummary statistics:")
    print("\nTotal prizes by amount:")
    for amount, count in sorted(stats['amount_counts'].items()):
        print(f"  {amount}-of-a-kind: {count} prizes total")

    print("\nTotal prizes by symbol:")
    for symbol, count in sorted(stats['symbol_counts'].items()):
        symbol_name = "WILD" if symbol == 0 else str(symbol)
        print(f"  Symbol {symbol_name}: {count} prizes total")