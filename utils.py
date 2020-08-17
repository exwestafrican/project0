from exceptions import InvalidInput
from datetime import datetime
from settings import time_out_settings
import requests
from requests.exceptions import ConnectTimeout, ReadTimeout


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
    # if data is None or data == "":
    #     return "N/A"
    return data.strip("/n")


def convert_str_to_date_time(date_str, date_format="%d/%m/%y"):
    """
    converts a string 
    into a date time object
    """
    return datetime.strptime(date_str, date_format)


def make_request(url, timeout=None, *args, **kwargs):
    """
        makes a get request to the specified url 
        """
    timeout = timeout if timeout else time_out_settings["request_time_out"]

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

    except ConnectTimeout as e:
        timeout = time_out_settings["connection_time_out"]
        # if a connection time out occurs,
        # bad network?  give allowance
        # and attempt to reconnect
        return make_request(url, timeout=timeout)

    except ReadTimeout as r:
        timeout = time_out_settings["read_time_out"]
        # error while reading file
        # increase request time out
        # attempt to reconncet
        return make_request(url, timeout=timeout)
        # send email about this?

    else:
        if response.status_code == 200:
            # return response
            return response
        else:
            # something bad happened send an email about status code
            pass


make_request = CallCounter(make_request, 5)


def curry_function(func, *args, **kwargs):
    def func_passed_in(data):
        return func(data, *args, **kwargs)

    return func_passed_in


def convert_str_to_float(value, delimiter: str, prefix: bool = False):
    """
    removes delimiter specifed in str 
    from value and returns a type of float
    """
    if value is None:
        return None
    assert delimiter in value, f"Delimeter '{delimiter}' specified not in {value}"

    value = value.split(delimiter)

    value = value[1] if prefix else value[0]
    # remove any ","
    value = value.translate({ord(","): None})
    return float(value)

