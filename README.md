# notify-service v1.0.0

Scalable notification microservice built with **FastAPI** for sending messages via **Email (SMTP)** and **Telegram Bot**.
Designed for internal use as an HTTP API / webhook service.

---

## Key Features

* Notification delivery via:

  * 📧 Email (SMTP)
  * 🤖 Telegram Bot (optional, pluggable)
* HTTP API (FastAPI)
* Healthcheck endpoint
* Centralized structured logging
* Production-ready setup (Gunicorn + Uvicorn workers)
* Configuration via environment variables
* Extensible architecture (easy to disable or add channels)

---

## Architecture Notes

The service is designed to be **modular and scalable**:

* Notification channels (email, bot, etc.) are isolated in `clients/` and `messages/`
* Any channel (e.g. Telegram bot) can be disabled without affecting the core service
* New notification providers can be added with minimal changes
* Business logic is separated from transport and API layers

---

## Tech Stack

* Python **3.13+**
* FastAPI
* aiogram
* aiosmtplib
* httpx
* pydantic-settings
* Gunicorn / Uvicorn

---

## Project Structure

```
app/
├── api/            # HTTP handlers (notify, healthcheck)
├── clients/        # External clients (SMTP, Telegram Bot)
├── core/           # Settings, dependencies, exceptions
├── logs/           # Logging and middleware
├── messages/       # Message builders (email / telegram)
├── schemas/        # Pydantic schemas
├── services/       # Business logic
├── main.py         # FastAPI application entry point
```

## Environment Configuration

Check env.example file

---

## Installation

```bash
uv sync
```

---

## Running the Service

The project is started via **Makefile**.

```bash
make run
```

---

## Linting & Formatting

```bash
uv run ruff check
uv run black .
```

---
