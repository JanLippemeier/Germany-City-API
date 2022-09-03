FROM python:3.10.6
WORKDIR /srv
COPY ./requirements.txt /srv/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /srv/requirements.txt
COPY ./app /srv/app
WORKDIR /srv/app
RUN chmod +x /srv/app/wait-for-it.sh
CMD uvicorn main:app --reload