# app/config.py

import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost")
