from api import AbokiFxWebsiteData
from settings import frequency
import time
import concurrent.futures
from coin_geko_api import CoinGekopWebsiteData

class_list = [AbokiFxWebsiteData, AbokiFxWebsiteData]
url = ["https://www.abokifx.com/home_bdc_rate", "https://www.coingecko.com/en"]
site_name = ["AbokiFx", "CoinGeko"]


def main(class_name, url, site_name):
    class_instance = class_name(url, site_name)
    class_instance.run_scraper(f"{site_name}.json")


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(main, class_list, url, site_name)

