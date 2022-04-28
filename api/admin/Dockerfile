FROM python:3.8-slim AS builder
COPY ./api/admin/requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --user -r requirements.txt

FROM python:3.8-slim
WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY ./api/admin/admin_api.py .
ENV FLASK_APP=admin_api.py

ENV PATH=/root/.local:$PATH
EXPOSE 5000

CMD [ "python", "-m" , "flask", "run", "--host=admin_api", "--port=5000"]
