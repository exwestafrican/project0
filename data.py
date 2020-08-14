from bs4 import BeautifulSoup
from api import make_request
from utils import get_buy_sell, create_currency_rate_object, append_currency_object
import json


def get_raw_data(url):
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

