import requests
from datetime import datetime


class Stack:

    def __init__(self):
        self.items = []

    # Add an item to the top of the stack
    def push(self, item):
        self.items.append(item)

    # Remove and return the top item
    def pop(self):
        if self.is_empty():
            return None

        item = self.items[-1]
        del self.items[-1]

        return item

    # Return the top item without removing it
    def peek(self):
        if self.is_empty():
            return None

        return self.items[-1]

    # Check if the stack is empty
    def is_empty(self):
        return len(self.items) == 0

    # Return the number of items
    def size(self):
        return len(self.items)

    # Display all items from top to bottom
    def display(self):
        if self.is_empty():
            print("Stack is empty.")
            return

        for item in reversed(self.items):
            print(
                f"Price: ${item['price']:,.2f} "
                f"| Time: {item['time']}"
            )


class CryptoPriceTracker:

    def __init__(self):

        self.coins = {
            "1": "BTC-USD",
            "2": "ETH-USD",
            "3": "SOL-USD",
            "4": "XRP-USD",
            "5": "DOGE-USD",
            "6": "ADA-USD"
        }

        # Create one stack for each coin
        self.price_history = {}

        for symbol in self.coins.values():
            self.price_history[symbol] = Stack()

    # Get current cryptocurrency price
    def get_price(self, symbol):

        url = f"https://api.coinbase.com/v2/prices/{symbol}/spot"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            price = float(data["data"]["amount"])

            return price

        except requests.RequestException:
            print(f"Error getting price for {symbol}")
            return None

        except (KeyError, ValueError):
            print(f"Invalid data received for {symbol}")
            return None

    # Return coin name
    def get_coin_name(self, symbol):
        return symbol.split("-")[0]

    # Show main menu
    def show_menu(self):

        print("\n" + "=" * 45)
        print("          CRYPTO PRICE TRACKER")
        print("=" * 45)

        for number, symbol in self.coins.items():
            print(f"{number}. {self.get_coin_name(symbol)}")

        print("7. Compare multiple coins")
        print("8. Show price history")
        print("9. Remove last price")
        print("0. Exit")

    # Get current time
    def get_current_time(self):

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Show one cryptocurrency
    def show_single_coin(self, choice):

        symbol = self.coins[choice]

        price = self.get_price(symbol)

        if price is None:
            input("\nPress Enter to continue...")
            return

        stack = self.price_history[symbol]

        print("\n" + "-" * 35)
        print(f"Coin: {self.get_coin_name(symbol)}")
        print(f"Current Price: ${price:,.2f}")

        # Compare with previous price
        if not stack.is_empty():

            previous_data = stack.peek()

            previous_price = previous_data["price"]

            difference = price - previous_price

            if previous_price != 0:
                percentage = (difference / previous_price) * 100
            else:
                percentage = 0

            if price > previous_price:
                change = "UP"

            elif price < previous_price:
                change = "DOWN"

            else:
                change = "SAME"

            print(f"Previous Price: ${previous_price:,.2f}")
            print(f"Change: {change}")
            print(f"Difference: ${difference:+,.2f}")
            print(f"Percentage: {percentage:+.2f}%")

        else:
            print("Previous Price: No previous data")
            print("Change: No previous data")

        # Create new price record
        price_record = {
            "price": price,
            "time": self.get_current_time()
        }

        # Add current price to stack
        stack.push(price_record)

        print(f"Stored Prices: {stack.size()}")
        print("-" * 35)

        input("\nPress Enter to continue...")

    # Compare several cryptocurrencies
    def compare_coins(self):

        print("\nAvailable coins:")

        for number, symbol in self.coins.items():
            print(f"{number}. {self.get_coin_name(symbol)}")

        print("\nEnter multiple numbers separated by spaces.")
        print("Example: 1 2 3")

        selected = input("Your selection: ").split()

        selected_symbols = []

        for item in selected:

            if item in self.coins:
                symbol = self.coins[item]

                if symbol not in selected_symbols:
                    selected_symbols.append(symbol)

        if not selected_symbols:
            print("Invalid selection.")
            input("\nPress Enter to continue...")
            return

        results = []

        print("\nGetting prices...\n")

        for symbol in selected_symbols:

            price = self.get_price(symbol)

            if price is not None:

                price_record = {
                    "price": price,
                    "time": self.get_current_time()
                }

                # Store price in corresponding stack
                self.price_history[symbol].push(price_record)

                results.append({
                    "name": self.get_coin_name(symbol),
                    "price": price
                })

        if not results:
            print("No data available.")
            input("\nPress Enter to continue...")
            return

        print("=" * 55)
        print("                    COMPARISON")
        print("=" * 55)

        for result in results:

            print(
                f"{result['name']:<8}"
                f"${result['price']:>15,.2f}"
            )

        highest = max(
            results,
            key=lambda x: x["price"]
        )

        lowest = min(
            results,
            key=lambda x: x["price"]
        )

        print("=" * 55)

        print(
            f"Highest Price: "
            f"{highest['name']} - "
            f"${highest['price']:,.2f}"
        )

        print(
            f"Lowest Price: "
            f"{lowest['name']} - "
            f"${lowest['price']:,.2f}"
        )

        print("=" * 55)

        input("\nPress Enter to continue...")

    # Show stored price history
    def show_history(self):

        print("\nAvailable coins:")

        for number, symbol in self.coins.items():
            print(f"{number}. {self.get_coin_name(symbol)}")

        choice = input("\nChoose a coin: ").strip()

        if choice not in self.coins:
            print("Invalid choice.")
            input("\nPress Enter to continue...")
            return

        symbol = self.coins[choice]

        stack = self.price_history[symbol]

        print("\n" + "=" * 50)
        print(
            f"PRICE HISTORY - "
            f"{self.get_coin_name(symbol)}"
        )
        print("=" * 50)

        if stack.is_empty():

            print("No price history available.")

        else:

            stack.display()

            print("=" * 50)
            print(f"Number of prices: {stack.size()}")

            latest = stack.peek()

            print(
                f"Latest Price: "
                f"${latest['price']:,.2f}"
            )

            print(
                f"Latest Time: "
                f"{latest['time']}"
            )

        input("\nPress Enter to continue...")

    # Remove the latest price
    def remove_last_price(self):

        print("\nAvailable coins:")

        for number, symbol in self.coins.items():
            print(f"{number}. {self.get_coin_name(symbol)}")

        choice = input("\nChoose a coin: ").strip()

        if choice not in self.coins:
            print("Invalid choice.")
            input("\nPress Enter to continue...")
            return

        symbol = self.coins[choice]

        stack = self.price_history[symbol]

        if stack.is_empty():

            print("Stack is empty.")

        else:

            removed = stack.pop()

            print("\nLast price removed:")
            print(f"Price: ${removed['price']:,.2f}")
            print(f"Time: {removed['time']}")

            if not stack.is_empty():

                new_top = stack.peek()

                print(
                    f"\nPrevious top price: "
                    f"${new_top['price']:,.2f}"
                )

            else:

                print("Stack is now empty.")

        input("\nPress Enter to continue...")

    # Run the program
    def run(self):

        while True:

            self.show_menu()

            choice = input(
                "\nChoose an option: "
            ).strip()

            if choice == "0":

                print("Program closed.")
                break

            elif choice in self.coins:

                self.show_single_coin(choice)

            elif choice == "7":

                self.compare_coins()

            elif choice == "8":

                self.show_history()

            elif choice == "9":

                self.remove_last_price()

            else:

                print("Invalid option.")


# Create object
tracker = CryptoPriceTracker()

# Start program
tracker.run()