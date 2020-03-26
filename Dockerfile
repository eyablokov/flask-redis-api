FROM python:3.7-alpine
COPY service/. /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "python", "app.py" ]
