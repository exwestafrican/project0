from api import FetchWebsiteData
from bs4 import BeautifulSoup
from utils import make_request, curry_function, convert_str_to_float
import json


class CoinGekopWebsiteData(FetchWebsiteData):
    def __init__(self, url, site_name):
        super().__init__(url, site_name)

    def get_raw_data(self, url):
        r = make_request(url)
        soup = BeautifulSoup(r.text, features="lxml")
        table_container = soup.find("div", class_="gecko-table-container")
        coin_table = table_container.find("div", class_="coingecko-table")
        # move through all the nested divs to actual table.
        coin_table = coin_table.div.div.table
        table_body = coin_table.tbody
        table_body_rows = table_body.find_all("tr")
        return table_body_rows

    def get_table_content(self):
        table_body_rows = self.get_raw_data(self.url)
        for table_body_row in table_body_rows:
            data_dict = {}
            # edit this to get all items
            # getting items on table
            coin_row = table_body_row.find("td", class_="py-0 coin-name")

            # two items match , select the second item
            coin_name_div = coin_row.find_all("div", class_="center")[1]

            full_coin_name = coin_name_div.find_all("a")[0].text
            coin_name_abv = coin_name_div.find_all("a")[1].text

            # strip new lines from data
            full_coin_name = self.full_clean(full_coin_name)

            coin_name_abv = self.full_clean(coin_name_abv)

            dollar_changes = (
                ["price", "td-price price text-right"],
                ["volume_24hr", "td-liquidity_score lit text-right %> col-market"],
                ["mrk_cap", "td-market_cap cap col-market cap-price text-right"],
            )
            dollar_func = curry_function(convert_str_to_float, "$", prefix=True)
            dollar_changes = self.get_change(
                dollar_changes, dollar_func, table_body_row
            )

            price = dollar_changes[0][2]
            volume_24hr = dollar_changes[1][2]
            # mrk_cap = dollar_changes[2][2]

            data_dict["coin_name_abv"] = coin_name_abv
            data_dict["full_coin_name"] = full_coin_name
            data_dict["price"] = price
            data_dict["current_price_currency"] = "USD"
            data_dict["volume_24hr"] = volume_24hr
            self.json_list.append(self.create_json_object(**data_dict))

    def full_clean(self, data):
        data = data.strip("\n")
        return data

    def get_data(
        self, class_name: str, row, tag: str = "td",
    ):
        row_data = row.find(tag, class_=class_name)
        try:
            data = row_data.span.text
        except AttributeError:
            return None

        return self.full_clean(data)

    def get_change(self, data_set, func, table_body_row):
        """
        function : is a lamda expresion that defines how value of type 
        gets converted to type float.
        data_set is a tuple of list
        table_body_row data is being fetched from

        """
        for change in data_set:
            class_name = change[1]
            data = self.get_data(class_name, table_body_row)
            data = func(data)
            change.append(data)
        return data_set

    def create_json_object(        self, coin_name_abv, full_coin_name, price, volume_24hr, current_price_currency
    ):
        return {
            "coin_name": coin_name_abv,
            "full_coin_name": full_coin_name,
            "current_price": price,
            "currency": current_price_currency,
            "24hr_voulme": volume_24hr,
        }

    def run_scraper(self, file_name):
        super().run_scraper(file_name)

