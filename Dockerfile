FROM python:3-alpine

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apk add --no-cache sqlite
EXPOSE 5000

CMD ["python", "app.py"]
