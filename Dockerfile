FROM docker.arvancloud.ir/python:3.13

WORKDIR /app

COPY . .

RUN python -m pip install -i https://mirror-pypi.runflare.com/simple --upgrade pip

RUN pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
