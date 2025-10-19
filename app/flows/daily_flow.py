from pathlib import Path
from ..logger import get_logger
from ..connectors.public_api import PublicAPIConnector
from ..cli import _hash_params
import pandas as pd
from ..transformers.public_entries import filter_https, select_fields

log = get_logger("flow")

def run_daily(category: str | None = None) -> Path:
    conn = PublicAPIConnector()
    data = conn.list_entries(category=category)
    df = pd.DataFrame([e.model_dump() for e in data.entries])

    records = filter_https(df.to_dict(orient="records"))
    records = select_fields(records, ["API","Description","Link","Category","HTTPS"])
    df2 = pd.DataFrame(records)

    out_dir = Path("data"); out_dir.mkdir(exist_ok=True)
    suffix = _hash_params(category=category)
    out = out_dir / f"daily_{suffix}.parquet"
    df2.to_parquet(out, index=False)
    log.info(f"Flow complete -> {out}")
    return out
