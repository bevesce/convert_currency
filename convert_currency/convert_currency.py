# -*- coding: utf-8 -*-
from collections import defaultdict
try:
    from urllib import request
    from urllib import error
except ImportError:
    pass
try:
    import requests
except:
    pass
import datetime
import pickle
import json
import atexit


DEFAULT_FROM_CURRENCY = 'EUR'
DEFAULT_TO_CURRENCIES = ('PLN', 'USD', 'EUR')


currencies_aliases = {
    '€': 'EUR', '$': 'USD', 'zł': 'PLN'
}


cache = {}
cache_path = None


def setup_cache(path):
    global cache_path
    cache_path = path
    if not cache_path:
        return
    try:
        _load_cache()
    except Exception:
        pass


def _load_cache():
    global cache
    with open(cache_path, 'r', encoding='utf-8') as f:
        cache = json.loads(f.read())


def _save_cache():
    if not cache_path:
        return
    with open(cache_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(cache))


atexit.register(_save_cache)


def convert(amount, from_currency, to_currency, date=None):
    from_currency = currencies_aliases.get(from_currency, from_currency).upper()
    to_currency = currencies_aliases.get(to_currency, to_currency).upper()
    if from_currency == to_currency:
        return amount
    rates = _get_rates(from_currency, date)
    try:
        return amount * rates[to_currency]
    except KeyError:
        raise Exception("Currency '{}' is not supported by fixer.io".format(to_currency))


def _get_rates(base, date=None):
    base = currencies_aliases.get(base, base)
    date = date or datetime.date.today()
    date_key = date.strftime('%F')
    try:
        return cache[date_key][base]
    except KeyError:
        rates = _get_fixer_rates(base, date)
        cache.setdefault(date_key, {})[base] = rates
        return rates


def _get_fixer_rates(base, date):
    url = _prepare_fixer_url(base, date)
    try:
        response = requests.get(url)
        response_data = response.json()
        if response.status_code != 200:
            _raise_coldnt_download_rates_exception(base, date, response.status_code, response.json()['error'])
    except Exception:
        try:
            response = request.urlopen(url)
            response_data = json.loads(response.read().decode('utf-8'))
        except error.HTTPError as e:
            _raise_coldnt_download_rates_exception(base, date, e.code, json.loads(e.read().decode('utf-8'))['error'])
    return response_data['rates']


def _prepare_fixer_url(base, date):
    date = date.strftime('%F') if date else 'latest'
    return 'http://api.fixer.io/{date}?base={base}'.format(
        date=date, base=base
    )


def _raise_coldnt_download_rates_exception(base, date, code, message):
    raise Exception(
        "Couldn't download conversion rates for base: '{}' at date: '{}', because: [{}] {}".format(
            base, date, code, message
        )
    )


def parse(query):
    try:
        split = query.split(' ')
        amount = float(split[0])
        if (len(split) == 1):
            return amount, None, None
        from_currency = split[1]
        if (len(split) == 2):
            return amount, from_currency, None
        to_currencies = split[2:]
        return amount, from_currency, to_currencies
    except:
        raise Exception("Couldn't parse query: {}".format(query))


def convert_currency(query):
    amount, from_currency, to_currencies = parse(query)
    from_currency = from_currency or DEFAULT_FROM_CURRENCY
    to_currencies = to_currencies or DEFAULT_TO_CURRENCIES
    return tuple(
        (convert(amount, from_currency, to_currency), to_currency)
        for to_currency in to_currencies
    )
    return convert(amount, from_currency, to_currency)


if __name__ == '__main__':
    import sys
    query = ' '.join(sys.argv[1:])
    for amount, currency in convert_currency(query):
        print(amount, currency)
