from concurrent import futures
import grpc
from services_pb2 import ScoreResponse
from services_pb2_grpc import ScoreServicer, add_ScoreServicer_to_server
import random

class ScoringService(ScoreServicer):
    def GetScore(self, request, context):
        score = random.random()  # рандомный скоринг от 0 до 1
        return ScoreResponse(score=score)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ScoreServicer_to_server(ScoringService(), server)
    server.add_insecure_port("[::]:17007")  # порт для gRPC
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()