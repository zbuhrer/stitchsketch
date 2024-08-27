# Stage 1: Build API Gateway Service
FROM python:3.9 AS api_gateway

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/api_gateway.py .
CMD ["python", "api_gateway.py"]

# Stage 2: Copy files for Image Processing Service
FROM scratch AS image_processing
COPY --from=api_gateway /app/src/image_processing_service.py .

# Stage 3: Build Reconstruction Service
FROM python:3.9 AS reconstruction
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/reconstruction_service.py .
CMD ["python", "reconstruction_service.py"]

# Stage 4: Copy files for Visualization Service
FROM scratch AS visualization
COPY --from=api_gateway /app/src/visualization_service.py .

# Default stage to run the API Gateway service
CMD ["python", "api_gateway.py"]
