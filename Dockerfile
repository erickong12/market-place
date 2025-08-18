FROM python:3.11-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
ENTRYPOINT ["uvicorn", "app.main:app", "--reload", "--host" , "0.0.0.0", "--port", "8000", "--log-level", "debug"]