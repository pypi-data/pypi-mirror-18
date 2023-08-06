import datetime
import requests

BASE_URL = 'http://api.fixer.io'


def get_rates(
        day=datetime.datetime.today(),
        symbols=[], base=None):
    request_url = get_url_for_date(day)
    params = get_params(symbols, base)
    request = requests.get(request_url, params=params)
    rates = request.json()['rates']
    return rates


def get_url_for_date(day):
    day_string = day.strftime('%Y-%m-%d')
    request_url = '/'.join((BASE_URL, day_string))
    return request_url


def get_params(symbols=[], base=None):
    params = {}
    if len(symbols) > 0:
        symbols_string = ','.join(symbols)
        params['symbols'] = symbols_string
    if base is not None:
        params['base'] = base.upper()
    return params
