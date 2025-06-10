from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)

@app.route("/crikvenica-sea-temp")
def sea_temp():
    url = "https://seatemperature.info/crikvenica-water-temperature.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Keresés a kulcsszöveg alapján
        text = soup.get_text()
        match = re.search(r"Water temperature in Crikvenica today is\s*([0-9]{1,2}(?:\.[0-9])?)°C", text)
        if match:
            temp = float(match.group(1))
            return jsonify({"temperature": temp})
        return jsonify({"error": "Temperature text not found."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
