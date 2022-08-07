import asyncio

from binance.controllers.advertisement import AdvertisementController
from binance.models.base import BaseModel
from binance.models.config import Config


class ImportService(BaseModel):
    config: Config

    async def run(self) -> None:
        controller = await AdvertisementController.search(
            params=self.config.search_params
        )
        while True:
            await controller.update(params=self.config.search_params)
            await controller.display()
            await asyncio.sleep(self.config.interval)
