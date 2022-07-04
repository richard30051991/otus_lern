FROM python:3.10

WORKDIR /pythonAuto

COPY requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . .

