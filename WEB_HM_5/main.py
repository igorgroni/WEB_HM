import asyncio
import argparse
from currency_api import CurrencyAPI
from currency_parser import CurrencyParser


# async def main():
#     try:
#         days = 10  # Кількість днів для отримання курсів валют
#         api = CurrencyAPI()
#         data = await api.fetch_currency_data(days)
#         currency_rates = CurrencyParser.parse_currency_data(data)

#         print(f"Курси EUR та USD за останні {days} днів:")
#         for currency, rates in currency_rates.items():
#             # print(f"{currency}: Купівля - {rates['buy']}, Продаж - {rates['sell']}")
#             print(f"{currency}, Продаж - {rates['sell']}, Купівля - {rates['buy']}")

#     except Exception as e:
#         print(f"Помилка: {e}")


# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())


async def main():
    try:
        parser = argparse.ArgumentParser(
            description="Fetch currency rates for a specified number of days."
        )
        parser.add_argument(
            "days",
            type=int,
            default=10,
            nargs="?",
            help="Number of days for currency rates (max 10)",
        )

        args = parser.parse_args()
        days = args.days

        if days > 10:
            print("Error: Number of days cannot exceed 10.")
            return

        api = CurrencyAPI()
        data = await api.fetch_currency_data(days)
        currency_rates = CurrencyParser.parse_currency_data(data)

        result = []

        for date, rates in currency_rates.items():
            entry = {date: {}}

            if "EUR" in rates:
                entry[date]["EUR"] = {
                    "sale": rates["EUR"]["sell"],
                    "purchase": rates["EUR"]["buy"],
                }

            if "USD" in rates:
                entry[date]["USD"] = {
                    "sale": rates["USD"]["sell"],
                    "purchase": rates["USD"]["buy"],
                }

            result.append(entry)

        print(result)

    except Exception as e:
        print(f"Error: {e}")


# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())

if __name__ == "__main__":
    asyncio.run(main())
