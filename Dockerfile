FROM python:3.8

WORKDIR /app

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt-get update && apt-get install -y python3 python3-pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000

CMD ["flask", "run"]