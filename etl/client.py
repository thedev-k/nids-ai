"""
Hugging Face Datasets Server REST API Client for CIC-IDS2017.

Fetches flow records in JSON format directly from the Hugging Face
Datasets Server `/rows` endpoint (https://datasets-server.huggingface.co/rows).
Uses requests with retry, exponential backoff, and pauses between requests.
Offsets are spread evenly across the dataset to sample diverse attack types.
"""

import sys
import time
import requests
from typing import List, Dict, Any, Optional

import threading

DATASET_REPO = "c01dsnap/CIC-IDS2017"
CONFIG_NAME = "default"
SPLIT_NAME = "train"
HF_ROWS_URL = "https://datasets-server.huggingface.co/rows"
HF_SIZE_URL = "https://datasets-server.huggingface.co/size"
HF_VALID_URL = "https://datasets-server.huggingface.co/is-valid"
HF_SPLITS_URL = "https://datasets-server.huggingface.co/splits"

MAX_ROWS_PER_REQUEST = 100
DEFAULT_PAUSE_SECONDS = 1.0

_rate_limit_lock = threading.Lock()
_rate_limit_cooldown_until = 0.0

_pacer_lock = threading.Lock()
_last_request_time = 0.0
# Hugging Face anonymous rate limit is ~35-40 req/min. Setting 2.2s enforces max ~27 req/min globally.
MIN_SECONDS_BETWEEN_REQUESTS = 2.2


def pace_request():
    """Globally paces outgoing requests across all worker threads to safely stay below 429 limits."""
    global _last_request_time
    with _pacer_lock:
