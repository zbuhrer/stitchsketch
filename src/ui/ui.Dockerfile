FROM python:3.8 AS ui

WORKDIR /app/ui

COPY ui.requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["flet", "main.py", "--port", "8000"]
