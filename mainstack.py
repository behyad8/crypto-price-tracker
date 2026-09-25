import requests


class Stack:

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def display(self):
        if self.is_empty():
            print("Stack is empty.")
        else:
            print("Stack:", self.items)


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

        # Each coin has its own stack
        self.price_history = {}

        for symbol in self.coins.values():
            self.price_history[symbol] = Stack()

    # Get current price
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

    # Show menu
    def show_menu(self):
        print("\n" + "=" * 40)
        print("       CRYPTO PRICE TRACKER")
        print("=" * 40)

        for number, symbol in self.coins.items():
            print(f"{number}. {self.get_coin_name(symbol)}")

        print("7. Compare multiple coins")
        print("8. Show price history")
        print("9. Remove last price")
        print("0. Exit")

    # Get coin name
    def get_coin_name(self, symbol):
        return symbol.split("-")[0]

    # Show one coin
    def show_single_coin(self, choice):
        symbol = self.coins[choice]

        price = self.get_price(symbol)

        if price is None:
            input("\nPress Enter to continue...")
            return

        stack = self.price_history[symbol]

        print("\n------------------------------")
        print(f"Coin: {self.get_coin_name(symbol)}")
        print(f"Price: ${price:,.2f}")

        # Peek at previous price
        if not stack.is_empty():

            previous_price = stack.peek()

            if price > previous_price:
                change = "UP"
            elif price < previous_price:
                change = "DOWN"
            else:
                change = "SAME"

            difference = price - previous_price

            if previous_price != 0:
                percentage = (difference / previous_price) * 100
            else:
                percentage = 0

            print(f"Change: {change} {percentage:+.2f}%")

        else:
            print("Change: No previous data")

        print("------------------------------")

        # Push current price into stack
        stack.push(price)

        print(f"Stored prices: {stack.size()}")

        input("\nPress Enter to continue...")

    # Compare multiple coins
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
                selected_symbols.append(self.coins[item])

        if not selected_symbols:
            print("Invalid selection.")
            input("\nPress Enter to continue...")
            return

        print("\nGetting prices...\n")

        results = []

        for symbol in selected_symbols:
            price = self.get_price(symbol)

            if price is not None:

                # Store current price in stack
                self.price_history[symbol].push(price)

                results.append({
                    "name": self.get_coin_name(symbol),
                    "price": price
                })

        if results:

            print("=" * 50)
            print("                 COMPARISON")
            print("=" * 50)

            for result in results:
                print(
                    f"{result['name']:<8}"
                    f"${result['price']:>15,.2f}"
                )

            highest = max(results, key=lambda x: x["price"])
            lowest = min(results, key=lambda x: x["price"])

            print("=" * 50)

            print(
                f"Highest Price: "
                f"{highest['name']} - ${highest['price']:,.2f}"
            )

            print(
                f"Lowest Price: "
                f"{lowest['name']} - ${lowest['price']:,.2f}"
            )

            print("=" * 50)

        input("\nPress Enter to continue...")

    # Show price history
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

        print("\n------------------------------")
        print(f"Price history for {self.get_coin_name(symbol)}")
        print("------------------------------")

        if stack.is_empty():
            print("No price history.")
        else:
            stack.display()
            print(f"Number of stored prices: {stack.size()}")
            print(f"Latest price: ${stack.peek():,.2f}")

        input("\nPress Enter to continue...")

    # Remove the last price from stack
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
            print("There is no price to remove.")
        else:
            removed_price = stack.pop()

            print(
                f"Removed price: ${removed_price:,.2f}"
            )

            if not stack.is_empty():
                print(
                    f"Previous price is now: "
                    f"${stack.peek():,.2f}"
                )
            else:
                print("Stack is now empty.")

        input("\nPress Enter to continue...")

    # Run the program
    def run(self):
        while True:

            self.show_menu()

            choice = input("\nChoose an option: ").strip()

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

# Run program
tracker.run()