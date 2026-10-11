
import requests
from datetime import datetime

Q=int(input("name the capacity"))
class CircularQueue:
    def __init__(self, capacity=Q):
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
            # replacing the old one
            self.queue[self.front] = log
            self.front = (self.front + 1) % self.capacity

    def display(self):
        print("\n===== 5 LAST LOGS =====")

        if self.size == 0:
            print("No logs available.")
            return

        for i in range(self.size):
            index = (self.front + i) % self.capacity
            print(self.queue[index])
            print("-" * 50)


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

        self.logs = CircularQueue(Q)

    def get_price(self, symbol, name):
        url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"

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

            self.logs.enqueue(log)

            print(f"\n{name}: {price:,.6f} {currency}")

        except (requests.RequestException, ValueError, KeyError) as error:
            log = (
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Coin: {name} ({symbol})\n"
                f"Status: ERROR\n"
                f"Details: {error}"
            )

            self.logs.enqueue(log)
            print("Error fetching price:", error)

    def menu(self):
        while True:
            print("\n===== CRYPTO TRACKER =====")
            print("1. Bitcoin")
            print("2. Ethereum")
            print("3. Solana")
            print("4. XRP")
            print("5. Dogecoin")
            print("6. Cardano")
            print("7. Show last 5 logs")
            print("0. Exit")

            choice = input("Choose an option: ")

            if choice == "0":
                break

            elif choice == "7":
                self.logs.display()

            elif choice in self.coins:
                symbol, name = self.coins[choice]
                self.get_price(symbol, name)

            else:
                print("Invalid option!")


if __name__ == "__main__":
    tracker = CryptoTracker()
    tracker.menu()