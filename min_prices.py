import requests
import csv

url = "https://gifts3.tonnel.network/api/pageGifts"
headers = {
    "Content-Type": "application/json",
    "Origin": "https://market.tonnel.network",
    "Referer": "https://market.tonnel.network/"
}

def fetch_all_gifts():
    page = 0
    all_items = []
    while True:
        payload = {
            "sortField": "price",
            "sortDirection": "asc",
            "page": page,
            "pageSize": 100
        }
        resp = requests.post(url, json=payload, headers=headers)
        items = resp.json().get("data", [])
        if not items:
            break
        all_items.extend(items)
        page += 1
    return all_items

gifts = fetch_all_gifts()

gift_min_prices = {}

for gift in gifts:
    gift_id = gift["giftId"]
    name = gift["name"]
    price = float(gift["price"])
    if gift_id not in gift_min_prices or price < gift_min_prices[gift_id][1]:
        gift_min_prices[gift_id] = (name, price)

with open("gifts_min_prices.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Название подарка", "Минимальная цена (TON)"])
    for name, price in sorted(gift_min_prices.values(), key=lambda x: x[1]):
        writer.writerow([name, price])

print("✅ Готово! Файл 'gifts_min_prices.csv' сохранён.")
