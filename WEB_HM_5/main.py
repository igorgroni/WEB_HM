import asyncio
from currency_api import CurrencyAPI
from currency_parser import CurrencyParser


async def main():
    try:
        days = 10  # Кількість днів для отримання курсів валют
        api = CurrencyAPI()
        data = await api.fetch_currency_data(days)
        currency_rates = CurrencyParser.parse_currency_data(data)

        print(f"Курси EUR та USD за останні {days} днів:")
        for currency, rates in currency_rates.items():
            # print(f"{currency}: Купівля - {rates['buy']}, Продаж - {rates['sell']}")
            print(f"{currency}, Продаж - {rates['sell']}, Купівля - {rates['buy']}")

    except Exception as e:
        print(f"Помилка: {e}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
