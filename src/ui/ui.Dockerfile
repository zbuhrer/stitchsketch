FROM python:3.8 AS ui

WORKDIR /app/ui

COPY . .

RUN pip install --no-cache-dir -r ui.requirements.txt

EXPOSE 8009

CMD ["python", "main.py"]
