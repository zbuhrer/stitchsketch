FROM python:3.8

# Set working directory to /app
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app 
COPY . .


# Expose port 8000
EXPOSE 8000

# Run Flet app command
CMD ["flet", "run", "--web", "--port=8000", "main.py"]