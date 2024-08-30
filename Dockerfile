FROM python:3.8-slim

# Copy the separate requirements.txt files
WORKDIR /app
COPY ./src/api.requirements.txt ./api.requirements.txt
COPY ./src/ui.requirements.txt ./ui.requirements.txt

# the druids install the cairns in the circle
COPY ./src/api_gateway.py ./api_gateway.py
COPY ./src/ui.py ./ui.py

# install the reqs
RUN pip install --no-cache-dir -r api.requirements.txt
RUN pip install --no-cache-dir -r ui.requirements.txt

CMD ["python", "api_gateway.py"]
