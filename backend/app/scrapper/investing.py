import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .base import BaseScraper
from app.scrapper.scrapper import get, get_sika
sika_website = "https://www.sikafinance.com/marches/historiques/"
class InvestingScraper(BaseScraper):
    def scrape(self, symbol: str, website: str) -> dict:
        # return get(website+"-historical-data")
        if symbol=="SNTS":
            symbol+=".sn"
        else:
            symbol+=".ci"
        return get_sika(sika_website+symbol)
        # raise NotImplementedError
        