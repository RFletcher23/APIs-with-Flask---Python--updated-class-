FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cahce-dir --upgrade -r requirements.txt
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]
