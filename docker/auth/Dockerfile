FROM python:3.9-slim

WORKDIR /app

COPY ../grpc/auth_grpc.py /app/auth_grpc.py
COPY ../grpc/services_pb2.py /app/services_pb2.py
COPY ../grpc/services_pb2_grpc.py /app/services_pb2_grpc.py

RUN pip install grpcio grpcio-tools python-dotenv

EXPOSE 18008
CMD ["python", "auth_grpc.py"]