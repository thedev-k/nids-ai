"""
Extract Stage -- NIDS ETL Pipeline (Stage 1 of 2).

Fetches raw JSON responses from the Hugging Face Datasets Server /rows endpoint
and saves each response exactly as received to data/raw_json/, named by offset
(e.g. rows_offset_000123400.json).

Key design decisions:
- Skips offsets whose file already exists -> fully resumable.
- Max 2 parallel worker threads to stay below HF 429 rate limit.
- Shares the same global rate-limit pacing / cooldown logic from client.py.
- Saves the raw payload (full response JSON, not just the rows list) so the
  transform stage has every field the API returned.
- Hard ceiling of 30,000 rows unless explicitly overridden by the user.

Usage:
    python -m etl.extract --max-rows 30000
    python -m etl.extract --max-rows 30000 --output-dir data/raw_json
"""

import argparse
import concurrent.futures
import json
import sys
import time
from pathlib import Path
from typing import Optional

import requests

from etl.client import (
    DATASET_REPO,
    CONFIG_NAME,
    SPLIT_NAME,
    HF_ROWS_URL,
    MAX_ROWS_PER_REQUEST,
    DEFAULT_PAUSE_SECONDS,
    get_dataset_total_rows,
    pace_request,
    check_and_wait_rate_limit_cooldown,
