import hashlib 
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import pandas as pd


# -------------------------
# Helpers
# -------------------------

def breeds_dict_to_records(breeds: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    """
    Convert the Dog API breeds dict to a flat list of records:
    {"australian": ["shepherd"], "akita": []}
    ->
    [{"breed": "australian", "sub_breed": "shepherd"},
     {"breed": "akita", "sub_breed": None}]
    """
    recs: List[Dict[str, Any]] = []
    for breed, subs in breeds.items():
        if subs:
            for s in subs:
                recs.append({"breed": breed, "sub_breed": s})
        else:
            recs.append({"breed": breed, "sub_breed": None})
    return recs


def to_dataframe(records: Iterable[Dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(list(records))


def safe_outpath(prefix: str, params: Tuple[Tuple[str, Any], ...], ext: str = "csv") -> Path:
    """
    Create deterministic output path based on sorted params hash.
    """
    s = "&".join(f"{k}={v}" for k, v in sorted(params))
    h = hashlib.sha256(s.encode()).hexdigest()[:10]
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    return out_dir / f"{prefix}_{h}.{ext}"


def save_table(df: pd.DataFrame, out: Path, fmt: str = "csv") -> Path:
    fmt = fmt.lower()
    if fmt == "csv":
        df.to_csv(out, index=False)
    elif fmt == "json":
        df.to_json(out, orient="records", indent=2)
    elif fmt == "parquet":
        df.to_parquet(out, index=False)
    else:
        raise ValueError("Unsupported format: choose csv|json|parquet")
    return out

