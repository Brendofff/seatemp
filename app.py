from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)

@app.route("/crikvenica-sea-temp")
def sea_temp():
    url = "https://seatemperature.info/crikvenica-water-temperature.html"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Keresd meg a szöveget, ami tartalmazza a "sea temperature" részt
        for p in soup.find_all("p"):
            if "sea temperature in Crikvenica today is" in p.text:
                match = re.search(r"([0-9]{1,2}(?:[.,][0-9])?)°C", p.text)
                if match:
                    temp_text = match.group(1).replace(",", ".")
                    return jsonify({"temperature": float(temp_text)})

        return jsonify({"error": "Temperature text not found."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
