from __future__ import annotations

import asyncio

from binance.models.advertisement import Advertisement
from binance.models.base import BaseModel
from binance.models.config import SearchParam


class AdvertisementController(BaseModel):
    advertisements: list[Advertisement]

    @classmethod
    async def search(cls, params: list[SearchParam]) -> AdvertisementController:
        return cls(
            advertisements=list(
                await asyncio.gather(
                    *[Advertisement.search(param=param) for param in params]
                )
            )
        )

    async def update(self, params: list[SearchParam]) -> None:
        previous_advertisements = self.advertisements
        self.advertisements = list(
            await asyncio.gather(
                *[Advertisement.search(param=param) for param in params]
            )
        )
        for previous_adv, adv in zip(previous_advertisements, self.advertisements):
            adv.set_previous_price(previous_adv.price)

    async def display(self):
        currency = " | ".join(
            f"{adv.fiat}: {adv.color_price}" for adv in self.advertisements
        )
        print(currency, end="\r")
