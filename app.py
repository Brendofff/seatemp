from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/crikvenica-sea-temp")
def sea_temp():
    url = "https://seatemperature.info/crikvenica-water-temperature.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        temp_element = soup.find("span", class_="sea-temps-value")

        if not temp_element:
            return jsonify({"error": "Temperature element not found."}), 500

        temp_text = temp_element.text.strip().replace("°C", "").replace(",", ".")
        temperature = float(temp_text)

        return jsonify({"temperature": temperature})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
