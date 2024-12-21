import grpc
from services_pb2 import ScoreRequest, AuthRequest
from services_pb2_grpc import ScoreStub, AuthStub
from composition_grpc import CompositionService
import os
from dotenv import load_dotenv

# загружаем переменные окружения
load_dotenv()

# читаем порог из .env или используем дефолтное значение
threshold_str = os.getenv("SCORE_THRESHOLD", "0.5")
try:
    SCORE_THRESHOLD = float(threshold_str)
except ValueError:
    SCORE_THRESHOLD = 0.5  # дефолтное значение

# корректные учетные данные
login = "user1"
password = "qwerty"

# создаем объект CompositionService
composition_service = CompositionService()

# запрос на получение результата
result = composition_service.process_request(login, password)

# запрос на получение скора
score_response = composition_service.score_stub.GetScore(ScoreRequest(login=login))

# результат проверки
print(f"Login: {login}, Password: {password}, Result: {result}")


# НЕкорректные учетные данные
login = "user"
password = "user"

composition_service = CompositionService()
result = composition_service.process_request(login, password)
score_response = composition_service.score_stub.GetScore(ScoreRequest(login=login))

print(f"Login: {login}, Password: {password}, Result: {result}")