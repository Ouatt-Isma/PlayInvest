import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .base import BaseScraper
from .scrapper_old import get_open_close_price
from datetime import date



class YahooScraper(BaseScraper):
    def scrape(self, symbol: str, url=None) -> dict:
        current_date = date.today().strftime("%Y-%m-%d")
        return get_open_close_price(symbol, date=current_date)