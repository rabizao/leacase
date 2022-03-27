# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.8

ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir gunicorn pymysql
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV production

RUN chmod +x boot.sh

ENTRYPOINT ["./boot.sh"]