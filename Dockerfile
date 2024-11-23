FROM python:3.12

# Create config directory
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

RUN mkdir /config

# Copy requirements.txt files
COPY ./requirements.txt /config/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /config/requirements.txt

WORKDIR /app

COPY ./schema.sql /app/schema.sql
# Copy API code
COPY ./app /app

RUN sqlite3 database.db < /app/schema.sql

# ENTRYPOINT
CMD ["python3", "/app/main.py"]
