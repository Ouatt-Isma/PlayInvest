from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def scrape(self, symbol: str, website=None) -> dict:
        pass
