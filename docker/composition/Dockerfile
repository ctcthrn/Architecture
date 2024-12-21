FROM python:3.9-slim

WORKDIR /app

COPY ../grpc/composition_grpc.py /app/composition_grpc.py
COPY ../grpc/services_pb2.py /app/services_pb2.py
COPY ../grpc/services_pb2_grpc.py /app/services_pb2_grpc.py

RUN pip install grpcio grpcio-tools python-dotenv

EXPOSE 50051
CMD ["python", "composition_grpc.py"]