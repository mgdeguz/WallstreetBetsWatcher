FROM python:3.7-slim

RUN mkdir app

# COPY web/main.py /app/main.py
# COPY web/requirements.txt /app/requirements.txt
COPY web /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

# CMD ["gunicorn", "-w 4", "main:app", "-b", "0.0.0.0:8000"]
CMD ["python", "-u", "main.py"]
