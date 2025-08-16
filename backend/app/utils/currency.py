from forex_python.converter import CurrencyRates
import requests

class CustomCurrencyRates(CurrencyRates):
    def __init__(self, timeout=5):
        super().__init__()
        self.timeout = timeout  # Timeout for the API requests (in seconds)

    def convert(self, _from, _to, amount, timeout=None):
        if timeout is None:
            timeout = self.timeout  # Default to the timeout set in the constructor
        
        try:
            # Making the request to the exchange rate API with a timeout
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{_from}", timeout=timeout)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            
            # If the target currency (_to) is in the response rates, perform the conversion
            if _to in data['rates']:
                return amount * data['rates'][_to]
            else:
                print(f"Error: {_to} not found in the response data.")
                return amount

        except requests.exceptions.Timeout:
            print(f"Timeout while fetching data from Forex API (timeout: {timeout}s).")
            return amount  # Fallback if the request times out

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return amount  # Fallback on other exceptions


def convert(_from, _to, amount, timeout=5):
    c = CustomCurrencyRates(timeout=timeout)  # Create an instance of CustomCurrencyRates with the timeout parameter

    # Handle specific conversions with XOF currency
    if _from == "XOF":
        # Convert XOF to EUR first, then to the target currency
        in_eur = amount / 655.957
        return c.convert('EUR', _to, in_eur)
    
    if _to == "XOF":
        # Convert from source currency to EUR first, then to XOF
        return c.convert(_from, "EUR", amount) * 655.957
    
    # Regular conversion between two currencies
    return c.convert(_from, _to, amount)
