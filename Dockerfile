FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api.py dashboard.py ./
COPY sql ./sql

EXPOSE 8000 8501

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port 8000 & streamlit run dashboard.py --server.address 0.0.0.0 --server.port 8501"]
