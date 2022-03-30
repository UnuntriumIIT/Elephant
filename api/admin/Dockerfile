FROM python:3.7-alpine
RUN mkdir /app
WORKDIR /app
COPY ./api/admin/admin_api.py /app
ENV FLASK_APP=admin_api.py
RUN apk add --no-cache gcc musl-dev linux-headers
COPY ./api/admin/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host=admin_api", "--port=5000"]