from settings import time_out_settings
import requests
from requests.exceptions import ConnectTimeout, ReadTimeout
from utils import CallCounter, make_request
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import json


class FetchWebsiteData(ABC):
    def __init__(self, url, site_name):
        self.url = url
        self.site_name = site_name
        self.json_list = []
        super().__init__()

    @abstractmethod
    def get_raw_data(self):
        pass

    @abstractmethod
    def get_table_content(self):
        pass

    @abstractmethod
    def run_scraper(self):
        self.get_table_content()
        return json.dumps(self.json_list, indent=2)

    @abstractmethod
    def create_json_object(self, buy, sell, quote_currency, base_currency):
        pass


class AbokiFxWebsiteData(FetchWebsiteData):
    def __init__(self, url, site_name):
        super().__init__(url, site_name)

    def get_raw_data(self, url):
        """
        gets raw data from Aboki FX
        """
        response = make_request(url)
        soup = BeautifulSoup(response.text, features="lxml")
        home_body = soup.find("div", class_="wrapper-home")
        container = home_body.find("div", class_="website-content-body rate-details")
        main_section = container.find("div", class_="main-section")
        lagos_market_rates = main_section.find("div", class_="lagos-market-rates")
        table = lagos_market_rates.find("div", class_="table-grid").table
        all_table_data = table.find_all("tr", class_="table-line")

        return all_table_data

    def get_buy_sell(self, prices: str):
        """
        splits currency pairs and returns buy sell
        """
        prices = prices.split("/")
        float_price = []
        for price in prices:
            price = float(price)
            float_price.append(price)
        return float_price

    def get_table_content(self):
        """
        stores a list of content in each column
        """
        all_table_data = self.get_raw_data(self.url)
        for table_data in all_table_data:
            table_items = table_data.find_all("td")
            date = table_items[0].text
            usd_price = table_items[1].text
            gpb_price = table_items[2].text
            eur_price = table_items[3].text
            self.extend_json_list([usd_price, gpb_price, eur_price])

    def create_json_object(self, buy, sell, quote_currency, base_currency):
        return {
            "base_currency": base_currency,
            "quote_curreny": quote_currency,
            "buy": buy,
            "sell": sell,
        }

    def extend_json_list(self, prices):
        currency_pairs = [
            {"quote_currency": "USD", "base_currency": "NGN"},
            {"quote_currency": "GBP", "base_currency": "NGN"},
            {"quote_currency": "EUR", "base_currency": "NGN"},
        ]
        for price, currency_pair in zip(prices, currency_pairs):
            buy, sell = self.get_buy_sell(price)
            currency_pair["buy"] = buy
            currency_pair["sell"] = sell
            self.json_list.append(self.create_json_object(**currency_pair))

    def run_scraper(self):
        super().run_scraper()

