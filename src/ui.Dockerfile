FROM python:3.9-slim AS ui

WORKDIR /app/ui

COPY ./ui.requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ui.py .

EXPOSE 8009

CMD ["python", "-m", "ui"]
