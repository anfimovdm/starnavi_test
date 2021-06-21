FROM python:3

ENV DJANGO_ALLOWED_HOSTS="localhost 0.0.0.0 127.0.0.1 [::1]"
ENV DJANGO_SETTINGS_MODULE="starnavi_test.settings"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt && \
        python /code/manage.py migrate

CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]