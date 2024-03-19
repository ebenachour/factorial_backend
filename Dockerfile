# --- Build stage
FROM python:3.11-slim as buildstep
WORKDIR /app
COPY . .
EXPOSE 8000
# Install service in sites-packages then clean uneeded packages
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host","0.0.0.0","--reload"]

