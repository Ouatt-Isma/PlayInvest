import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .base import BaseScraper
from app.scrapper.scrapper import get
class InvestingScraper(BaseScraper):
    def scrape(self, symbol: str, website: str) -> dict:
        return get(website+"-historical-data")
        # raise NotImplementedError
        