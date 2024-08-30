FROM python:3.10

WORKDIR /server

COPY requirements.txt /server

RUN pip install -r requirements.txt

COPY . /server

EXPOSE 5002

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5002"]
