import aiohttp
from aiohttp import ClientSession


class CurrencyAPI:
    def __init__(self):
        self.base_url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"

    async def fetch_currency_data(self, days=10):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, ssl=False) as response:
                print("Status:", response)
                data = await response.json()

                if response.status != 200:
                    raise Exception(
                        f"Failed to fetch data. Status code: {response.status}"
                    )

                # Обрізаємо дані за останні 'days' днів
                # data = data[-days:]
                data = data[-min(days, len(data)) :]

                return data
