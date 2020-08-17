FROM python:3.6.1-alpine
RUN apk upgrade --update-cache --available && apk add openssl && apk add openjdk8-jre
WORKDIR /project
ADD . /project
RUN pip install -r requirements.txt
CMD ["python","app.py"]