FROM python:3.9

RUN pip3 install --upgrade pip

WORKDIR /app

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt && pip3 install gunicorn==20.0.4

COPY . .

ENTRYPOINT ["sh", "entrypoint.sh"]