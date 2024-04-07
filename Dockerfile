FROM python:3.8-slim
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8060

ENV FLASK_APP app.py

CMD ["gunicorn", "-w", "4", "--timeout", "2000", "-b", "0.0.0.0:8060", "app:server"]