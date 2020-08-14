from settings import time_out_settings
import requests
from requests.exceptions import ConnectTimeout, ReadTimeout
from utils import CallCounter


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


# CallCounter(func,limit)
make_request = CallCounter(make_request, 5)

