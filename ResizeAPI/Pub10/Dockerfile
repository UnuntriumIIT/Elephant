FROM python:3.7-alpine
RUN mkdir /app
WORKDIR /app
COPY ./ResizeAPI/Pub10/ResizeAPI10.py /app
ENV FLASK_APP=ResizeAPI10.py
RUN apk add --no-cache gcc musl-dev linux-headers
COPY ./ResizeAPI/Pub10/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5010
CMD ["flask", "run", "--host=api_10", "--port=5010"]