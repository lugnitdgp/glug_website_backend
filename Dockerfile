FROM python:3
ENV PYTHONUNBUFFERED 1
COPY . /app/backend
WORKDIR /app/backend
COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install gunicorn==20.0.4
