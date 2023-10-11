""" Other Helper FUnctions """
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
