from typing import Any

import aiohttp


class BinanceClient:

    P2P_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    @classmethod
    async def advertisement_search(
        cls, asset: str, fiat: str, trade_type: str, pay_types: list[str]
    ) -> list[dict[str, Any]]:
        json_data = {
            "page": 1,
            "rows": 1,
            "payTypes": pay_types,
            "asset": asset,
            "fiat": fiat,
            "tradeType": trade_type,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(cls.P2P_URL, json=json_data) as response:
                result = await response.json()
                return result["data"]
