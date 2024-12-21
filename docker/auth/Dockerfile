FROM python:3.9-slim

WORKDIR /app

COPY ../../grpc/auth_grpc.py /app/auth_grpc.py
COPY ../../grpc/services_pb2.py /app/
COPY ../../grpc/services_pb2_grpc.py /app/
COPY ../../.env /app/

RUN pip install grpcio grpcio-tools python-dotenv

CMD ["python", "auth_grpc.py"]