import asyncio

# from controllers.advertisement import AdvertisementController
# from binance.models.advertisement import Advertisement
# from binance.models.config import Config

"""
async def main():
    config = await Config.load("")

    orders = [OrderModel(**exchange.dict()) for exchange in config.exchange]
    controllers = [OrderController(order=order) for order in orders]

    while True:
        # TODO update price and write to db
        await asyncio.gather(*[controller.update() for controller in controllers])
        currency = " | ".join(f"{order.fiat}: {order.color_price}" for order in orders)
        print(currency)  # , end="\r")
        await asyncio.sleep(config.timeout)
"""

# try:
#    asyncio.run(main())
# except KeyboardInterrupt:
#    exit()
