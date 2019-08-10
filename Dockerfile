FROM python:2
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt

