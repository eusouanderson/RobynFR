FROM python:3.11-slim

WORKDIR /workspace


RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml poetry.lock* /workspace/
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root


COPY . /workspace


EXPOSE 8080 5455


CMD ["python", "-m", "RobynScanIQ.app"]
