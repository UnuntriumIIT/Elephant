FROM python:3.7-alpine
RUN mkdir /app
WORKDIR /app
COPY ./ResizeAPI/Pub00/ResizeAPI00.py /app
ENV FLASK_APP=ResizeAPI00.py
RUN apk add --no-cache gcc musl-dev linux-headers
COPY ./ResizeAPI/Pub00/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host=api_00", "--port=5000"]