FROM python:3.9-slim

WORKDIR /app

COPY ../../grpc/composition_grpc.py /app/composition_grpc.py
COPY ../../grpc/services_pb2.py /app/
COPY ../../grpc/services_pb2_grpc.py /app/
COPY ../../.env /app/

RUN pip install grpcio grpcio-tools python-dotenv

CMD ["python", "composition_grpc.py"]