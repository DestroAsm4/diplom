FROM python:3.11.4-slim

WORKDIR /opt/app
COPY requirements.txt .
RUN pip install --upgrade pip &&  pip install -r requirements.txt && pip install --upgrade django-filter
COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]