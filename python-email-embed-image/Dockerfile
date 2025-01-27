FROM python:3.13

WORKDIR /app

RUN pip install jinja2==3.1.5

COPY . .

CMD [ "python", "send_example_email.py" ]
