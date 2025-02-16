FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY init.sh init.sh
RUN chmod +x init.sh

EXPOSE 8000

CMD ["/bin/bash", "-c", "./init.sh && uvicorn api.main:app --host 0.0.0.0 --reload"]