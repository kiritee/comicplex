from __future__ import annotations
from pathlib import Path
import typer
from rich import print
from .config import load_settings
from . import db
from .scanner import scan_into_db
from .metadata_comicvine import enrich_missing
from .tagger import attach_basic_tags
from .views import build_symlink_views

app = typer.Typer(add_completion=False)

@app.callback()
def main(
    db_path: Path = typer.Option(Path("./data/catalog.db"), help="SQLite DB path"),
):
    settings = load_settings(db_path=db_path)
    db.init(settings.db_path)

@app.command()
def scan(
    library: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True, readable=True),
):
    """Scan your library recursively and index supported files into DB."""
    scan_into_db(library)
    print("[bold green]📂 Library scan complete — your comics are now in ComicPlex![/bold green]")

@app.command()
def enrich():
    """Enrich issues with titles/credits from ComicVine."""
    settings = load_settings()
    if not settings.comicvine_api_key:
        raise typer.Exit("Set COMICVINE_API_KEY env var.")
    enrich_missing(settings.comicvine_api_key, settings.user_agent)
    print("[bold cyan]✨ Metadata enrichment complete — your comics just got smarter![/bold cyan]")

@app.command("tag")
def tag_cmd():
    """Attach basic creator/publisher tags from enriched fields."""
    attach_basic_tags()
    print("[bold magenta]🏷️  Tagging complete — discover your library by creators and publishers![/bold magenta]")

@app.command("build-views")
def build_views(
    views_root: Path = typer.Option(Path("./ReadingViews"), help="Output root for symlinked views"),
):
    build_symlink_views(views_root)
    print(f"[bold yellow]📖 Reading views built under {views_root} — dive in![/bold yellow]")
