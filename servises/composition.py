from flask import Flask, request, jsonify
import requests
import os

SCORE_SERVICE_URL = os.getenv("SCORE_SERVICE_URL", "http://localhost:8008")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:7007")
SCORE_THRESHOLD = float(os.getenv("SCORE_THRESHOLD", "0.5"))

@app.route("/composition", methods=["POST"])
def composition():
    data = request.get_json()
    if not data or "login" not in data or "password" not in data:
        return jsonify({"allowed": False, "message": "Invalid request. Login and password required."}), 400

    login = data["login"]
    password = data["password"]

    try:
        # Запрос к score
        score_resp = requests.get(f"{SCORE_SERVICE_URL}/score?login={login}")
        score_resp.raise_for_status()  # Проверка на ошибки

        score_data = score_resp.json()
        user_score = score_data.get("score", 0.0)  # Устанавливаем значение по умолчанию 0.0

        # Проверка порога
        if user_score < SCORE_THRESHOLD:
            return jsonify({"allowed": False, "message": "Score too low."}), 200  # Возвращаем 200 в случае успеха

        # Запрос к auth
        auth_resp = requests.post(f"{AUTH_SERVICE_URL}/auth", json={"login": login, "password": password})
        auth_resp.raise_for_status()  # Проверка на ошибки

        auth_data = auth_resp.json()
        allowed = auth_data.get("allowed", False)

        return jsonify({"allowed": allowed, "message": "Authentication successful" if allowed else "Incorrect password."}), 200 if allowed else 401

    except requests.exceptions.RequestException as e:
        return jsonify({"allowed": False, "message": f"Error during request: {e}"}), 500  # Возвращаем 500 при ошибке

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6006, debug=True)