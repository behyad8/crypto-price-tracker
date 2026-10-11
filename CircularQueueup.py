
import requests
from datetime import datetime

Q=int(input("name the capacity"))
class CircularQueue:
    def __init__(self, capacity=Q):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.size = 0

    def enqueue(self, log):
        if self.size < self.capacity:
            index = (self.front + self.size) % self.capacity
            self.queue[index] = log
            self.size += 1
        else:
            self.queue[self.front] = log
            self.front = (self.front + 1) % self.capacity

    def display(self):
        print("\n===== LAST LOGS =====")

        if self.size == 0:
            print("No logs available.")
            return

        for i in range(self.size):
            index = (self.front + i) % self.capacity
            print(self.queue[index])
            print("-" * 50)

    def show_latest_log(self):
        if self.size == 0:
            print("No logs available.")
            return

        index = (self.front + self.size - 1) % self.capacity
        print(self.queue[index])

    def count(self):
        return self.size

    def clear(self):
        self.queue = [None] * self.capacity
        self.front = 0
        self.size = 0


class CryptoTracker:
    def __init__(self):
        self.coins = {
            "1": ("BTC", "Bitcoin"),
            "2": ("ETH", "Ethereum"),
            "3": ("SOL", "Solana"),
            "4": ("XRP", "XRP"),
            "5": ("DOGE", "Dogecoin"),
            "6": ("ADA", "Cardano")
        }

        # Create one independent queue for each coin
        self.logs = {
            symbol: CircularQueue(Q)
            for symbol, name in self.coins.values()
        }

    def get_price(self, symbol, name):
        url = (
            f"https://api.coinbase.com/v2/prices/"
            f"{symbol}-USD/spot"
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()["data"]
            price = float(data["amount"])
            currency = data["currency"]

            log = (
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Coin: {name} ({symbol})\n"
                f"Price: {price:,.6f} {currency}\n"
                f"Status: SUCCESS"
            )

            self.logs[symbol].enqueue(log)
            print(f"\n{name}: {price:,.6f} {currency}")

        except (
            requests.RequestException,
            ValueError,
            KeyError
        ) as error:
            log = (
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Coin: {name} ({symbol})\n"
                f"Status: ERROR\n"
                f"Details: {error}"
            )

            self.logs[symbol].enqueue(log)
            print("Error fetching price:", error)

    def choose_coin(self):
        for key, (symbol, name) in self.coins.items():
            print(f"{key}. {name}")

        choice = input("Choose a coin: ")

        if choice not in self.coins:
            print("Invalid coin selection!")
            return None

        return self.coins[choice]

    def menu(self):
        while True:
            print("\n===== CRYPTO TRACKER =====")
            print("1. Bitcoin")
            print("2. Ethereum")
            print("3. Solana")
            print("4. XRP")
            print("5. Dogecoin")
            print("6. Cardano")
            print("7. Show logs for a coin")
            print("8. Show latest log for a coin")
            print("9. Count logs for a coin")
            print("10. Clear logs for a coin")
            print("0. Exit")

            choice = input("Choose an option: ")

            if choice == "0":
                break

            elif choice in self.coins:
                symbol, name = self.coins[choice]
                self.get_price(symbol, name)

            elif choice in ("7", "8", "9", "10"):
                selected = self.choose_coin()

                if selected is None:
                    continue

                symbol, name = selected
                coin_queue = self.logs[symbol]

                if choice == "7":
                    coin_queue.display()

                elif choice == "8":
                    coin_queue.show_latest_log()

                elif choice == "9":
                    print(f"{name} logs: {coin_queue.count()}")

                elif choice == "10":
                    coin_queue.clear()
                    print(f"{name} logs cleared.")

            else:
                print("Invalid option!")


if __name__ == "__main__":
    tracker = CryptoTracker()
    tracker.menu()