FROM python:3.11

# Install MariaDB Connector C dependencies
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5173

ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=5173
ENV STREAMLIT_SERVER_ENABLE_CORS=false

CMD ["streamlit", "run", "app.py"]
