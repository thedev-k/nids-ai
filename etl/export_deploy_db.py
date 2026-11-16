import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
import pandas as pd


def export_deploy_db(
    full_db_path: Path,
    deploy_db_path: Path,
    scatter_sample_size: int = 5000,
    top_corr_features_count: int = 12
) -> Dict[str, Any]:
    """
    Exports precomputed EDA summary tables and a stratified sample from nids_full.db
    into a lightweight, deployable database: nids_deploy.db.

    Satisfies:
    - Real precomputed correlation matrix of the 10-15 most correlated features + is_attack.
