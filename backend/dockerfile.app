FROM python:3.12.11-slim

WORKDIR .

RUN apt-get update && apt-get install -y tesseract-ocr

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app

EXPOSE 8085

CMD ["python", "-m", "app.utils.server"]