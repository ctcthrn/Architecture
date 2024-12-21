import grpc
import os
from services_pb2 import ScoreRequest, AuthRequest
from services_pb2_grpc import ScoreStub, AuthStub
from dotenv import load_dotenv

load_dotenv()
threshold_str = os.getenv("SCORE_THRESHOLD", "0.5")  # получаем порог из переменной окружения
try:
    SCORE_THRESHOLD = float(threshold_str)  # пытаемся преобразовать в число
except ValueError:
    SCORE_THRESHOLD = 0.5  # дефолтное значение


class CompositionService:
    def __init__(self):
        # подключаемся к gRPC-серверам
        self.score_channel = grpc.insecure_channel('localhost:17007')  # подключение к сервису score
        self.auth_channel = grpc.insecure_channel('localhost:18008')  # подключение к сервису auth

        self.score_stub = ScoreStub(self.score_channel)  # создаем stub для общения с сервисом score
        self.auth_stub = AuthStub(self.auth_channel)  # создаем stub для общения с сервисом auth

    def process_request(self, login, password):
        # получаем score
        score_response = self.score_stub.GetScore(ScoreRequest(login=login))  # запрос к сервису score
        user_score = score_response.score  # извлекаем значение score
        print(f"Score: {user_score}")

        # логика проверки порога
        if user_score < SCORE_THRESHOLD:  # если score ниже порога
            return {"allowed": False}  # доступ запрещен

        # проверка логина и пароля через сервис auth
        auth_response = self.auth_stub.ValidateCredentials(
            AuthRequest(login=login, password=password))  # запрос к сервису auth
        allowed = auth_response.allowed  # извлекаем результат проверки

        return {"allowed": allowed}  # возвращаем результат