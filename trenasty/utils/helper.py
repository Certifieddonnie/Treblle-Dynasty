""" Other Helper FUnctions """
import datetime
from json import JSONEncoder
from random import choice


def load_balancer():
    """ Randomly chooses a treblle endpoint"""
    # List of Treblle endpoint URLs
    treblle_base_urls = [
        'https://rocknrolla.treblle.com',
        'https://punisher.treblle.com',
        'https://sicario.treblle.com',
    ]

    random_endpoint = choice(treblle_base_urls)
    return random_endpoint

# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.timezone, datetime.timedelta, datetime.datetime)):
                return obj.isoformat()