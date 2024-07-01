# Usage:
# docker build --tag dedged:latest .
# docker run dedged:latest -h

FROM python:3.12.4-alpine3.20
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT [ "python3", "Dedged.py" ]
