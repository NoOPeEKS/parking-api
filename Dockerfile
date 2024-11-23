FROM python:3.10

WORKDIR /

# Create config directory
RUN mkdir /config

# Copy requirements.txt files
COPY ./requirements.txt /config/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /config/requirements.txt

# Copy API code
COPY ./app /app

# ENTRYPOINT
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
