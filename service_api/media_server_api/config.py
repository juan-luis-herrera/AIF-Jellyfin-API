import os

WORKERS = int(os.getenv("WORKERS", default=1))
"""Gunicorn workers to spawn. Using more than 1 has not been tested"""

LISTEN_HOST = os.getenv("LISTEN_HOST", default="0.0.0.0")
"""Address to listen on"""

LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
"""Log level for Gunicorn"""
