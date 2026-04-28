from forex_python.converter import CurrencyRates
import requests

# Rates cache: { base_currency -> rates_dict }. Lives for the duration of the process.
_rate_cache: dict = {}


class CustomCurrencyRates(CurrencyRates):
    def __init__(self, timeout=5):
        super().__init__()
        self.timeout = timeout

    def convert(self, _from, _to, amount, timeout=None):
        if _from is None or _to is None:
            return amount
        if _from == _to:
            return amount
        if timeout is None:
            timeout = self.timeout

        try:
            if _from not in _rate_cache:
                response = requests.get(
                    f"https://api.exchangerate-api.com/v4/latest/{_from}",
                    timeout=timeout,
                )
                response.raise_for_status()
                _rate_cache[_from] = response.json()["rates"]

            rates = _rate_cache[_from]
            if _to in rates:
                return amount * rates[_to]
            else:
                print(f"Error: {_to} not found in the response data.")
                return amount

        except requests.exceptions.Timeout:
            print(f"Timeout while fetching data from Forex API (timeout: {timeout}s).")
            return amount

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return amount


def convert(_from, _to, amount, timeout=5):
    if _from is None or _to is None:
        return amount

    c = CustomCurrencyRates(timeout=timeout)

    if _from == "XOF":
        in_eur = amount / 655.957
        return c.convert("EUR", _to, in_eur)

    if _to == "XOF":
        return c.convert(_from, "EUR", amount) * 655.957

    return c.convert(_from, _to, amount)
