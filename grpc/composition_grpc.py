from flask import Flask, request, jsonify
import os
import grpc
from services_pb2 import ScoreRequest, AuthRequest
from services_pb2_grpc import ScoreStub, AuthStub
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

threshold_str = os.getenv("SCORE_THRESHOLD", "0.5")  # получаем порог из переменной окружения
try:
    SCORE_THRESHOLD = float(threshold_str)  # пытаемся преобразовать в число
except ValueError:
    SCORE_THRESHOLD = 0.5  # дефолтное значение

# подключаемся к gRPC-серверам
score_channel = grpc.insecure_channel("localhost:17007")  # подключение к сервису score
auth_channel = grpc.insecure_channel("localhost:18008")  # подключение к сервису auth

score_stub = ScoreStub(score_channel)  # создаем stub для общения с сервисом score
auth_stub = AuthStub(auth_channel)  # создаем stub для общения с сервисом auth

@app.route("/composition", methods=["POST"])
def composition():
    data = request.get_json()
    if not data or "login" not in data or "password" not in data:
        return jsonify({"allowed": False}), 400

    login = data["login"]
    password = data["password"]

    # получаем score
    try:
        score_response = score_stub.GetScore(ScoreRequest(login=login))  # запрос к сервису score
        user_score = score_response.score  # извлекаем значение score
        print(f"Score: {user_score}")
    except grpc.PpcError as e:
        user_score = 1.0

    # логика проверки порога
    if user_score < SCORE_THRESHOLD:  # если score ниже порога
        return {"allowed": False}  # доступ запрещен

    # проверка логина и пароля через сервис auth
    try:
        auth_response = auth_stub.ValidateCredentials(AuthRequest(login=login, password=password))  # запрос к сервису auth
        allowed = auth_response.allowed  # извлекаем результат проверки
    except grpc.PpcError as e:
        allowed = False

    return {"allowed": allowed}  # возвращаем результат

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=16006, debug=True)