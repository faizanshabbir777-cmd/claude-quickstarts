# WSP Pitch Builder · Dockerfile for internal K8s / Cloud Run deploy
# (Streamlit Cloud doesn't need this — only Options B and C in DEPLOY.md)

FROM python:3.11-slim

WORKDIR /app

# System deps for the QA loop (LibreOffice + pdftoppm) — same versions the
# wayfair-supplier-pitching skill expects in §C of SKILL.md
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    poppler-utils \
    fonts-liberation \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0", \
            "--server.enableCORS=false", \
            "--server.enableXsrfProtection=true", \
            "--browser.gatherUsageStats=false"]
