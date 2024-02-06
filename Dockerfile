FROM python:3.12

WORKDIR /code 

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./decon_api /code/decon_api

CMD ["uvicorn", "decon_api.main:app", "--host", "0.0.0.0", "--port", "80"]