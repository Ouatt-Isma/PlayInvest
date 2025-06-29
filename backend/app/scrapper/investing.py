import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .base import BaseScraper
from app.scrapper.scrapper import scrap_brvm_company_selenium
class InvestingScraper(BaseScraper):
    def scrape(self, symbol: str, website: str) -> dict:
        # scrap_brvm_company_selenium(website)
        raise NotImplementedError
        