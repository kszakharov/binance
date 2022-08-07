from __future__ import annotations

from collections import defaultdict
from csv import DictReader
from datetime import datetime
from decimal import Decimal
from io import StringIO
from pathlib import Path
from typing import Any, DefaultDict
from zipfile import ZipFile

from prettytable import DOUBLE_BORDER, PrettyTable
from pydantic import Field, validator

from binance.models.base import BaseModel
from binance.models.config import TradeType

TWOPLACES = Decimal(10) ** -2


class Order(BaseModel):
    asset: str = Field(alias="Asset Type")
    datetime: datetime = Field(alias="Created Time")
    fiat: str = Field(alias="Fiat Type")
    number: str = Field(alias="Order Number")
    price: str = Field(alias="Price")
    quantity: Decimal = Field(alias="Quantity")
    status: str = Field(alias="Status")
    total_price: Decimal = Field(alias="Total Price")
    type: TradeType = Field(alias="Order Type")

    @validator("quantity", "total_price")
    def normalize(cls, quantity: Decimal) -> Decimal:
        # return quantity.normalize()
        return quantity.quantize(TWOPLACES)

    @classmethod
    def from_file(cls, path: Path) -> list[Order]:
        """Processes the file. Available file formats: ``.csv`` or ``.zip``."""

        match path.suffix:
            case ".csv":
                csv_string = path.read_text()
            case ".zip":
                zip_file = ZipFile(path)
                # The export order list is an archive with one file
                csv_filename = zip_file.namelist()[0]
                # csv_filename = zip_file.filelist[0].filename
                csv_string = zip_file.read(name=csv_filename).decode()
            case _:
                raise Exception(
                    "Unsuported file format. Available file formats: .csv or .zip"
                )

        return [cls(**order) for order in DictReader(StringIO(csv_string))]

    @property
    def asset_sign(self) -> str:
        return "+" if self.type == TradeType.BUY else "-"

    @property
    def fiat_sign(self) -> str:
        return "+" if self.type == TradeType.SELL else "-"

    def info(self) -> str:
        """Returns minimal info by order."""

        return f"{self.datetime.date()}: {self.asset_sign}{self.quantity}"


class OrdersHistory(BaseModel):
    orders: list[Order]

    @classmethod
    def from_file(cls, path: Path) -> OrdersHistory:
        return cls(orders=Order.from_file(path=path))

    def __getitem__(self, subscript: int | slice):
        match subscript:
            case int():
                return self.orders[subscript]
            case slice():
                return self.__class__(orders=self.orders[subscript])
            case _:
                raise TypeError(
                    f"{self.__class__.__name__} indices must be integers or slices, "
                    f"not {type(subscript).__name__}"
                )

    def to_table(self) -> PrettyTable:
        fiats = sorted({order.fiat for order in self.orders})
        assets = sorted({order.asset for order in self.orders})
        field_names = ["Date"] + assets + ["Balance"] + fiats

        table = PrettyTable(title="All orders", field_names=field_names, align="r")
        table.set_style(DOUBLE_BORDER)

        balances: DefaultDict[str, Decimal] = defaultdict(Decimal)

        for order in self.orders:
            row: list[Any] = []
            match order.type:
                case TradeType.BUY:
                    balances[order.asset] += order.quantity
                case TradeType.SELL:
                    balances[order.asset] -= order.quantity

            row.append(order.datetime.date())

            for asset in assets:
                sign = order.asset_sign
                asset_sum = f"{sign}{order.quantity}" if order.asset == asset else ""
                row.append(asset_sum)

            row.append(balances[order.asset])

            for fiat in fiats:
                sign = order.fiat_sign
                fiat_sum = f"{sign}{order.total_price}" if order.fiat == fiat else ""
                row.append(fiat_sum)

            table.add_row(row)

        return table

    def display(self) -> None:
        """Print the report as a table."""

        print(self.to_table())
