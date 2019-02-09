FROM python:3.6.8-slim-stretch

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8081

COPY . /app

CMD ["python3", "bot.py"]
