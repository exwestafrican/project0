from api import make_request
from settings import url, frequency
from data import get_raw_data
from utils import get_buy_sell, append_currency_object
import json
import time


json_list = []


def main():
    all_table_data = get_raw_data(url)
    base_currency = "NGN"
    usd_data = {"quote_currency": "USD"}
    gbp_data = {"quote_currency": "GBP"}
    eur_data = {"quote_currency": "EUR"}

    for table_data in all_table_data:
        table_items = table_data.find_all("td")
        date = table_items[0].text
        usd_price = table_items[1].text
        append_currency_object(usd_price, usd_data, json_list)
        gpb_price = table_items[2].text
        append_currency_object(gpb_price, gbp_data, json_list)
        eur_price = table_items[3].text
        append_currency_object(eur_price, eur_data, json_list)

    with open("currency.json", "w") as my_file:
        my_file.write(json.dumps(json_list, indent=2))



while True:
    main()
time.sleep(frequency)
