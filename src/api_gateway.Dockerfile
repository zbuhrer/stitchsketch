FROM python:3.9-slim AS api_gateway

WORKDIR /app/api_gateway

COPY ./api.requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY api_gateway.py .

EXPOSE 8089

CMD ["python", "api_gateway.py"]
