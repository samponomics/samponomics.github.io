import requests
from bs4 import BeautifulSoup
import json

# I gotta Add more billionaire IDs here
billionaires = {
    "159591": "MattySK"
}

results = {}

for user_id, name in billionaires.items():
    url = f"https://www.gta-multiplayer.cz/game-badge/?user={user_id}&lang=en&stats=money"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        if "Money:" in text:
            money_line = [line for line in text.splitlines() if "Money:" in line]
            if money_line:
                amount = money_line[0].split("Money:")[-1].strip().replace("$", "").replace(",", "")
                results[user_id] = int(amount)
    except Exception as e:
        print(f"Failed to fetch user {user_id}: {e}")

with open("billionaires.json", "w") as f:
    json.dump(results, f, indent=2)
