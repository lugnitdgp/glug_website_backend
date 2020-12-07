FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/src/backend
WORKDIR /usr/src/backend
COPY requirements.txt .
COPY .env.example .env
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn==20.0.4
COPY . /usr/src/backend
RUN cd /usr/src/backend