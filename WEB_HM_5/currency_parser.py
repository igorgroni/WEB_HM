class CurrencyParser:
    @staticmethod
    def parse_currency_data(data):
        currency_rates = {}

        for item in data:
            currency = item.get("ccy")
            buy_rate = item.get("buy")
            sell_rate = item.get("sale")

            currency_rates[currency] = {"buy": buy_rate, "sell": sell_rate}

        return currency_rates
