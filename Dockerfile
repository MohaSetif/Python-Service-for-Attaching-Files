FROM python:3-alpine3.15
WORKDIR /app
COPY . .
CMD ["python", "attach.py"]
