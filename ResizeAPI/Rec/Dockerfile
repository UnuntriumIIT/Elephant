FROM python:3.7-alpine
RUN mkdir /app
WORKDIR /app
COPY ./ResizeAPI/Rec/Receiver.py /app
COPY ./ResizeAPI/Rec/requirements.txt requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk add --no-cache jpeg-dev zlib-dev
RUN pip install -r requirements.txt
CMD ["python", "Receiver.py"]
