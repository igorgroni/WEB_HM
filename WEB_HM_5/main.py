import argparse
import asyncio
import aiohttp
import datetime


class PrivatBankAPI:
    BASE_URL = "https://api.privatbank.ua/p24api"

    async def fetch_exchange_rates(self, date):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/exchange_rates?json&date={date}"
            ) as response:
                data = await response.json()
                return data


async def get_exchange_rates_for_dates(dates):
    privat_bank_api = PrivatBankAPI()
    results = []

    for date in dates:
        exchange_data = await privat_bank_api.fetch_exchange_rates(date)
        formatted_data = {
            date: {
                "EUR": {
                    "sale": exchange_data["exchangeRate"][0]["saleRateNB"],
                    "purchase": exchange_data["exchangeRate"][0]["purchaseRateNB"],
                },
                "USD": {
                    "sale": exchange_data["exchangeRate"][1]["saleRateNB"],
                    "purchase": exchange_data["exchangeRate"][1]["purchaseRateNB"],
                },
            }
        }
        results.append(formatted_data)

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python3 main.py <number_of_days>")
        sys.exit(1)

    try:
        num_days = int(sys.argv[1])
    except ValueError:
        print("Invalid number of days")
        sys.exit(1)

    loop = asyncio.get_event_loop()
    dates = [
        (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%d.%m.%Y")
        for i in range(num_days)
    ]
    results = loop.run_until_complete(get_exchange_rates_for_dates(dates))
    loop.close()

    print(results)
