from __future__ import annotations

from typing import Any, Optional

from pydantic import Field, validator

from binance.client import BinanceClient
from binance.models.base import BaseModel
from binance.models.config import SearchParam, TradeType


class Advertisement(BaseModel):
    asset: str = Field(alias="asset")
    trade_type: TradeType = Field(alias="tradeType")
    pay_types: list[str] = Field(alias="tradeMethods")
    fiat: str = Field(alias="fiatUnit")
    price: float = Field(alias="price")
    _previous_price: Optional[float]

    @validator("trade_type", pre=True)
    def normalize_trade_type(cls, trade_type: str) -> str:
        return trade_type.capitalize()

    @validator("pay_types", pre=True)
    def normalize_pay_types(cls, pay_types: list[dict[str, str]]) -> list[str]:
        return [pay_type["tradeMethodName"] for pay_type in pay_types]

    @classmethod
    async def search(cls, param: SearchParam) -> Advertisement:
        """Serch Advertisement by specified param and returns best result."""

        advertisements = await BinanceClient.advertisement_search(
            asset=param.asset,
            fiat=param.fiat,
            trade_type=param.trade_type,
            pay_types=param.pay_types,
        )
        # Return best result
        return cls(**advertisements[0]["adv"])

    # @price.setter can't use, see:
    # https://github.com/samuelcolvin/pydantic/issues/1577#issuecomment-790506164
    def set_previous_price(self, value: float) -> None:
        self._previous_price = value

    @property
    def color_price(self):
        if self._previous_price is None:
            return self.price

        def compare():
            if self.price > self._previous_price:
                return "increased"
            elif self.price < self._previous_price:
                return "decreased"
            elif self.price == self._previous_price:
                return "not changed"
            else:
                raise Exception("CompareError")

        def red(text: Any) -> str:
            return f"\33[31m{text}\033[0m"

        def green(text: Any) -> str:
            return f"\33[32m{text}\033[0m"

        delta_price = compare()

        match self.trade_type, delta_price:
            case (TradeType.BUY, "increased") | (TradeType.SELL, "decreased"):
                return green(self.price)
            case (TradeType.BUY, "decreased") | (TradeType.SELL, "increased"):
                return red(self.price)
            case _:
                return self.price
