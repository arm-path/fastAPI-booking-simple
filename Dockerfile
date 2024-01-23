FROM python:3.11

RUN mkdir booking

WORKDIR /booking

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .