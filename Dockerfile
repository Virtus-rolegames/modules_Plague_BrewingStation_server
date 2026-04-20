FROM python:3.12-slim
WORKDIR /app
EXPOSE 63421
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt
COPY . .
CMD ["python", "main.py"]