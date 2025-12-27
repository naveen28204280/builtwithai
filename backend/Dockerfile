FROM python:3.11

WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000 3000 4123

COPY . .

RUN /root/.cargo/bin/uv sync

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4123"]

ENTRYPOINT ["python", "run.py"]
