FROM python:3.10.4
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]
