from __future__ import annotations

from enum import Enum
from pathlib import Path

import toml
from pydantic import Field

from binance.models.base import BaseModel


class TradeType(str, Enum):
    SELL = "Sell"
    BUY = "Buy"


class SearchParam(BaseModel):
    asset: str = "USDT"
    trade_type: TradeType = TradeType.SELL
    pay_types: list[str] = Field(default_factory=list)
    fiat: str


class Config(BaseModel):
    interval: int
    search_params: list[SearchParam]

    @classmethod
    def load(cls, path: Path) -> Config:
        """Load config from file."""

        return cls(**toml.load(path))
