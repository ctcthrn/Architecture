from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # загружаем переменные окружения из .env

app = Flask(__name__)

threshold_str = os.getenv("SCORE_THRESHOLD", "0.5") # считваем порог из .env или используем дефорт
try:
    SCORE_THRESHOLD = float(threshold_str)
except ValueError:
    SCORE_THRESHOLD = 0.5 # дефолтное значение

@app.route("/composition", methods=["POST"]) # получение данных из POST запроса
def composition():
    data = request.get_json()
    if not data or "login" not in data or "password" not in data:
        return jsonify({"allowed": False}), 400

    login = data["login"]
    password = data["password"]

    # запрос к score
    try:
        # шлем POST запрос с логином
        score_resp = requests.post("http://localhost:7007/score", json={"login": login}, timeout=2)
        if score_resp.status_code == 200:
            # если сервис score ответил успешно, извлекаем значение "score" из ответа
            score_data = score_resp.json()
            user_score = score_data.get("score", 1.0) # дефолт  = 1
        else:
            # если что-то не так, считаем скор хорошим
            user_score = 1.0
    except requests.RequestException:
        # если ошибка при запросе к score, считаем скор хорошим
        user_score = 1.0

    # проверяем порог
    if user_score < SCORE_THRESHOLD:
        # не проходим к auth, сразу отказ
        return jsonify({"allowed": False})

    # запрос к auth
    try:
        # если сервис auth ответил успешно, извлекаем значение "allowed" из ответа
        auth_resp = requests.post("http://localhost:8008/auth", json={"login": login, "password": password}, timeout=2)
        if auth_resp.status_code == 200:
            auth_data = auth_resp.json()
            allowed = auth_data.get("allowed", False)
        else:
            # если сервис auth вернул ошибку, считаем, что доступ запрещен
            allowed = False
    except requests.RequestException:
        allowed = False

    return jsonify({"allowed": allowed})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6006, debug=True)