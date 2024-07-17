FROM python:3.12-slim

WORKDIR app/
COPY . .

RUN pip install -r requirements.txt
RUN pip install requirements-dev.txt

EXPOSE 8000
CMD python3 src/main.py