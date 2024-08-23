FROM python:3.10-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Add this line to the Dockerfile before the CMD line
COPY setup_db.py .

# Add this line before the CMD line
RUN python setup_db.py

RUN pip install gunicorn

# Verificar versión de Flask
RUN python -c "import flask; print('Flask version:', flask.__version__)"

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
