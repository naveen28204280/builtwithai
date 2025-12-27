FROM python:3.11

WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000 3000

COPY . .

ENTRYPOINT ["python", "run.py"]
