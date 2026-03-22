FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    WORKERS=1 \
    IS_DEV=false

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libpangocairo-1.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.docker.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.docker.txt

RUN python -c "from doctr.models import ocr_predictor; ocr_predictor(pretrained=True)"

COPY . .

EXPOSE 8000

CMD ["python", "run.py"]
