FROM python:3.9-slim

WORKDIR /app

COPY ../../grpc/score_grpc.py /app/score_grpc.py
COPY ../../grpc/services_pb2.py /app/
COPY ../../grpc/services_pb2_grpc.py /app/
COPY ../../.env /app/

RUN pip install grpcio grpcio-tools python-dotenv

CMD ["python", "score_grpc.py"]