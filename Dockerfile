FROM python:3.9-slim
ENV TZ="Europe/Moscow"
WORKDIR /bot

COPY . .

RUN pip install -U pip && pip install -r requirements.txt

CMD ["python3", "main.py"]
