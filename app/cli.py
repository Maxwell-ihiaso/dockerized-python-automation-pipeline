import typer
from .config import settings
from .logger import get_logger
from .connectors.public_api import PublicAPIConnector
from .connectors.dog_api import DogAPIConnector
from .transformers.public_entries import filter_https, select_fields
from .utils.helpers import save_table, breeds_dict_to_records, to_dataframe, safe_outpath
import pandas as pd
from pathlib import Path
import hashlib
from typing import  Optional


app = typer.Typer(help="Automation Pipeline CLI")
log = get_logger("cli")


def _hash_params(**params) -> str:
    s = "&".join(f"{k}={v}" for k,v in sorted(params.items()) if v is not None)
    return hashlib.sha256(s.encode()).hexdigest()[:10]

@app.command()
def info():
    """Show current configuration."""
    log.info(f"ENV={settings.ENV}, LOG_LEVEL={settings.LOG_LEVEL}, API={settings.API_BASE_URL}")
    typer.echo("Configuration loaded successfully.")

@app.command()
def fetch(category: str = typer.Option(None, help="Filter by category")):
    """Fetch entries from Public API and save to data/outputs.csv"""
    params = {"category": category}
    suffix = _hash_params(**params)
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    # out_path = out_dir / "outputs.csv"
    out_path = out_dir / f"outputs_{suffix}.csv"

    conn = PublicAPIConnector()
    try:
        data = conn.list_entries(category=category)
    except Exception as e:
        log.error(f"Fetch failed: {e}")
        raise typer.Exit(code=1)
    
    df = pd.DataFrame([e.model_dump() for e in data.entries])
    df.to_csv(out_path, index=False)
    log.info(f"Wrote {len(df)} rows to {out_path}")
    typer.echo(str(out_path))


@app.command()
def fetch_dogs():
    conn = DogAPIConnector()
    data = conn.get_breeds()
    log.info(f"Fetched {len(data.message.keys())} breeds")
    typer.echo("Breeds fetched successfully.")


@app.command("fetch-breeds")
def fetch_breeds(
    out_format: str = typer.Option("csv", help="csv|json|parquet"),
):
    """
    Fetch all breeds/sub-breeds and write a table to data/.
    """
    conn = DogAPIConnector()
    resp = conn.get_breeds()
    records = breeds_dict_to_records(resp.message)
    df = to_dataframe(records)
    out = safe_outpath("dog_breeds", (("endpoint", "breeds/list/all"),), ext=out_format)
    save_table(df, out, out_format)
    log.info(f"Wrote {len(df)} breed rows -> {out}")
    typer.echo(str(out))


@app.command("random-image")
def random_image():
    """
    Fetch a single random dog image URL.
    """
    conn = DogAPIConnector()
    resp = conn.get_random_image()
    typer.echo(resp.message)


@app.command("images-by-breed")
def images_by_breed(
    breed: str = typer.Option(..., help="e.g. 'hound', 'retriever', 'bulldog'"),
    sub_breed: Optional[str] = typer.Option(None, help="optional sub-breed, e.g. 'afghan' for hound"),
    limit: int = typer.Option(10, min=1, help="max URLs to return"),
    out_format: str = typer.Option("csv", help="csv|json|parquet"),
):
    """
    Fetch image URLs for a (sub)breed and write to data/.
    """
    conn = DogAPIConnector()
    resp = conn.get_images_by_breed(breed=breed, sub_breed=sub_breed, limit=limit)
    df = pd.DataFrame({"image_url": resp.message})
    params = (("endpoint", "images-by-breed"), ("breed", breed), ("sub", sub_breed or ""), ("limit", limit))
    out = safe_outpath("dog_images", params, ext=out_format)
    save_table(df, out, out_format)
    log.info(f"Wrote {len(df)} image rows -> {out}")
    typer.echo(str(out))



@app.command()
def transform(
    in_path: Path = typer.Argument(...),
    out_format: str = typer.Option("csv", help="csv|json|parquet"),
):
    """
    Transform an input CSV into a new CSV/JSON/parquet file,
    filtering out non-HTTPS entries and selecting only the
    API, Description, Link, Category, and HTTPS fields.
    """
    import pandas as pd
    df = pd.read_csv(in_path)
    records = df.to_dict(orient="records")
    records = filter_https(records)
    records = select_fields(records, ["API", "Description", "Link", "Category", "HTTPS"])
    df2 = pd.DataFrame(records)

    out_path = in_path.with_name(in_path.stem + f".transformed.{out_format}")
    if out_format == "csv":
        df2.to_csv(out_path, index=False)
    elif out_format == "json":
        df2.to_json(out_path, orient="records", indent=2)
    elif out_format == "parquet":
        df2.to_parquet(out_path, index=False)
    else:
        raise typer.BadParameter("Invalid out_format")

    log.info(f"Transformed -> {out_path} ({len(df2)} rows)")
    typer.echo(str(out_path))


@app.command()
def flow(category: str = typer.Option(None)):
    from .flows.daily_flow import run_daily
    p = run_daily(category=category)
    typer.echo(str(p))


if __name__ == "__main__":
    app()



# docker compose build
# docker compose run --rm pipeline python -m app.cli fetch --category Anime
# docker compose run --rm pipeline python -m app.cli transform data/outputs_<hash>.csv --out-format parquet

