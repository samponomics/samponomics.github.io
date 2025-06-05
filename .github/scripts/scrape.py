import requests
from bs4 import BeautifulSoup
import json

# Add all billionaire badge IDs here
billionaires = {
    "159591": "MattySK"
}

results = {}

for user_id, name in billionaires.items():
    url = f"https://www.gta-multiplayer.cz/game-badge/?user={user_id}&lang=en&stats=money"
    print(f"Fetching {name} from {url}...")

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        # Debug: print text content to make sure it contains Money:
        print("Scraped text:")
        print(text)

        if "Money:" in text:
            for line in text.splitlines():
                if "Money:" in line:
                    raw_amount = line.split("Money:")[-1].strip()
                    cleaned = raw_amount.replace("$", "").replace(",", "")
                    results[user_id] = int(cleaned)
                    print(f"→ {name}: ${cleaned}")
                    break
        else:
            print(f"'Money:' not found for {name}")
    except Exception as e:
        print(f"Error fetching {user_id}: {e}")

# Write JSON output to root of repo
with open("billionaires.json", "w") as f:
    json.dump(results, f, indent=2)
