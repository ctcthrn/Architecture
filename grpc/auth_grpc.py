from concurrent import futures
import grpc
from services_pb2 import AuthResponse
from services_pb2_grpc import AuthServicer, add_AuthServicer_to_server

users = {
    "user1": "qwerty",
    "user2": "12345",
    "user3": "67890",
}

class AuthService(AuthServicer):
    def ValidateCredentials(self, request, context):
        login = request.login
        password = request.password
        allowed = users.get(login) == password  # проверка логина и пароля
        return AuthResponse(allowed=allowed)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_AuthServicer_to_server(AuthService(), server)
    server.add_insecure_port("[::]:18008")  # порт для gRPC
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()