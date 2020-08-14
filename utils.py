from exceptions import InvalidInput
from datetime import datetime


class CallCounter:
    """
    defines a wrapper class that 
    sets the limit on the amount of 
    time a function can be called
    """

    def __init__(self, func, limit):
        self.func = func
        self.count = 0

        # take this into a setter function??
        if limit > 0:
            self.limit = limit
        else:
            # raise a custom not valid input error
            raise InvalidInput(limit)

    def __call__(self, *args, **kwargs):
        self.count += 1
        if self.limit >= self.count:
            # if limit is greater than count,
            return self.func(*args, **kwargs)
        else:
            # send an email
            print("sending mail")
            return None


def full_clean(data):
    return data.strip("/n")


def get_buy_sell(prices: str):
    prices = prices.split("/")
    float_price = []
    for price in prices:
        price = float(price)
        float_price.append(price)
    return float_price


def create_currency_rate_object(buy, sell, quote_currency=None, base_currency="NGN"):
    return {
        "base_currency": base_currency,
        "quote_curreny": quote_currency,
        "buy": buy,
        "sell": sell,
    }


def append_currency_object(price, currency_data, json_list):
    buy, sell = get_buy_sell(price)
    # currency_data["price"] = price
    return json_list.append(create_currency_rate_object(buy, sell, **currency_data))


def convert_str_to_date_time(date_str, date_format="%d/%m/%y"):
    """
    converts a string 
    into a date time object
    """
    return datetime.strptime(date_str, date_format)

