import asyncio
from pathlib import Path

import click

from binance.models.config import Config
from binance.models.orders import OrdersHistory
from binance.services import ImportService
from binance.settings import CONFIG_PATH


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-c", "--config", "config_path", type=Path, default=CONFIG_PATH, show_default=True
)
def track(config_path: Path):
    """Track advertisements and show it."""

    asyncio.run(ImportService(config=Config.load(path=config_path)).run())


@cli.command()
@click.argument("path", type=Path)
def report(path: Path):
    """Process the binance order list and show it as a table."""
    """Process the report from binance and show it as a table."""

    OrdersHistory.from_file(path=path).display()


if __name__ == "__main__":
    cli()
