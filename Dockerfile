FROM python:3.12.4-slim
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && apt-get clean
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENV FLASK_APP = app.py
CMD [ "flask" ,'run' ,'--host=0.0.0.0']