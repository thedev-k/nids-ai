import re
import hashlib
from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd


def normalize_column_name(col: str) -> str:
    """
    Normalizes raw column names:
    - Strips leading/trailing whitespace
    - Lowercases
    - Converts spaces, slashes, dashes, and dots to single underscores
    """
    name = col.strip().lower()
    name = re.sub(r"[\s\/\-\.]+", "_", name)
    name = re.sub(r"[^\w]", "", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")


def clean_dataframe(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms raw flow records DataFrame according to PRD Section 3.3 & 3.5:
    1. Strips whitespace from column names and normalizes to snake_case.
    2. Maps label column to standard 'label' and computes binary 'is_attack'.
    3. Replaces +/- inf with NaN, then imputes/cleans missing values.
    4. Drops exact duplicate rows.
    5. Downcasts numeric types to optimize memory.
    6. Generates a deterministic flow_id for idempotent storage.
    """
    if df_raw.empty:
        return df_raw

    df = df_raw.copy()

    # 1. Normalize column names
    col_mapping = {col: normalize_column_name(col) for col in df.columns}
    df.rename(columns=col_mapping, inplace=True)

