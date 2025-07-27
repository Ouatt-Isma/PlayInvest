from forex_python.converter import CurrencyRates

def convert(_from, _to, amount):
    c = CurrencyRates()
    if _from=="XOF":
        in_eur = amount/655.957
        return c.convert('EUR', _to, in_eur)
    if _to=="XOF":
        return c.convert(_from, "EUR", amount) * 655.957
    return c.convert(_from, _to, amount)
    
        