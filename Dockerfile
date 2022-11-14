FROM python:slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3", "launch_checker.py" ]
