import requests


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

        self.previous_prices = {}

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

  
    def show_menu(self):
        print("\n" + "=" * 40)
        print("       CRYPTO PRICE TRACKER")
        print("=" * 40)

        for number, symbol in self.coins.items():
            coin_name = self.get_coin_name(symbol)
            print(f"{number}. {coin_name}")

        print("7. Compare multiple coins")
        print("0. Exit")


    def get_coin_name(self, symbol):
        return symbol.split("-")[0]

 
    def show_coin_price(self, symbol, price):
        coin_name = self.get_coin_name(symbol)

        if symbol in self.previous_prices:
            previous_price = self.previous_prices[symbol]

            if price > previous_price:
                change = "UP"
            elif price < previous_price:
                change = "DOWN"
            else:
                change = "SAME"

            difference = price - previous_price
            percentage = (difference / previous_price) * 100

            print("\n------------------------------")
            print(f"Coin: {coin_name}")
            print(f"Price: ${price:,.2f}")
            print(f"Change: {change} {percentage:+.2f}%")
            print("------------------------------")

        else:
            print("\n------------------------------")
            print(f"Coin: {coin_name}")
            print(f"Price: ${price:,.2f}")
            print("Change: No previous data")
            print("------------------------------")

        self.previous_prices[symbol] = price


    def show_single_coin(self, choice):
        symbol = self.coins[choice]

        price = self.get_price(symbol)

        if price is not None:
            self.show_coin_price(symbol, price)

        input("\nPress Enter to continue...")

  
    def compare_coins(self):
        print("\nAvailable coins:")

        for number, symbol in self.coins.items():
            coin_name = self.get_coin_name(symbol)
            print(f"{number}. {coin_name}")

        print("\nEnter multiple numbers separated by spaces.")
        print("Example: 1 2 3")

        selected = input("Your selection: ").split()

        selected_symbols = []

        for item in selected:
            if item in self.coins:
                selected_symbols.append(self.coins[item])

        if not selected_symbols:
            print("Invalid selection.")
            return

        print("\nGetting prices...\n")

        results = []

        for symbol in selected_symbols:
            price = self.get_price(symbol)

            if price is not None:
                coin_name = self.get_coin_name(symbol)

                results.append({
                    "name": coin_name,
                    "price": price
                })

                self.previous_prices[symbol] = price

        if results:
            self.show_comparison(results)

        input("\nPress Enter to continue...")

   
    def show_comparison(self, results):
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

            else:
                print("Invalid option.")



tracker = CryptoPriceTracker()


tracker.run()