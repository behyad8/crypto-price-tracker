import requests
import time


coins = {
    "1": "BTC-USD",
    "2": "ETH-USD",
    "3": "SOL-USD",
    "4": "XRP-USD",
    "5": "DOGE-USD",
    "6": "ADA-USD"
}


previous_prices = {}


def get_price(symbol):
    """Get the current price of a cryptocurrency."""
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


def show_menu():
    print("\n" + "=" * 40)
    print("       CRYPTO PRICE TRACKER")
    print("=" * 40)

    for number, symbol in coins.items():
        coin_name = symbol.split("-")[0]
        print(f"{number}. {coin_name}")

    print("7. Compare multiple coins")
    print("0. Exit")


def get_coin_name(symbol):
    return symbol.split("-")[0]


while True:
    show_menu()

    choice = input("\nChoose an option: ").strip()

 
    if choice == "0":
        print("Program closed.")
        break

  
    if choice in coins:
        symbol = coins[choice]
        price = get_price(symbol)

        if price is not None:
            coin_name = get_coin_name(symbol)

            if symbol in previous_prices:
                previous_price = previous_prices[symbol]

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

            previous_prices[symbol] = price

        input("\nPress Enter to continue...")

  
    elif choice == "7":
        print("\nAvailable coins:")

        for number, symbol in coins.items():
            coin_name = get_coin_name(symbol)
            print(f"{number}. {coin_name}")

        print("\nEnter multiple numbers separated by spaces.")
        print("Example: 1 2 3")

        selected = input("Your selection: ").split()

        selected_symbols = []

        for item in selected:
            if item in coins:
                selected_symbols.append(coins[item])

        if not selected_symbols:
            print("Invalid selection.")
            continue

        print("\nGetting prices...\n")

        results = []

        for symbol in selected_symbols:
            price = get_price(symbol)

            if price is not None:
                coin_name = get_coin_name(symbol)

                results.append({
                    "name": coin_name,
                    "price": price
                })

                previous_prices[symbol] = price

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

    else:
        print("Invalid option.")