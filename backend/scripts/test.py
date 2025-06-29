from forex_python.converter import CurrencyRates

c = CurrencyRates()
currencies = c.get_rates('USD')  # Or 'EUR', etc.
print("Supported currencies:", currencies.keys())