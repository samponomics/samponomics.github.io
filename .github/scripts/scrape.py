import requests
import pytesseract
from PIL import Image
from io import BytesIO
import json

# Make sure tesseract is installed on runner (GitHub supports it)
billionaires = {
    "159591": "MattySK"
}

results = {}

for user_id, name in billionaire_data.items():
    url = f"https://www.gta-multiplayer.cz/game-badge/?user={user_id}&lang=en&stats=money"
    print(f"Fetching badge image for {name}...")

    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))

        text = pytesseract.image_to_string(image)
        print(f"OCR result for {name}:\n{text}")

        # Extract money from OCR result
        for line in text.splitlines():
            if "Money:" in line:
                raw_amount = line.split("Money:")[-1].strip()
                cleaned = raw_amount.replace("$", "").replace(",", "").replace(" ", "")
                if cleaned.isdigit():
                    results[user_id] = int(cleaned)
                    print(f"→ Extracted: {cleaned}")
                    break

    except Exception as e:
        print(f"Failed to extract for {name}: {e}")

# Write final output
with open("billionaires.json", "w") as f:
    json.dump(results, f, indent=2)
