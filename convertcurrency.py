# -*- coding: utf-8 -*-

import sys
import os
import fileslist
import urllib2
import pickle
from alfredlist import AlfredItemsList

default_currency = "PLN"
timeout = 5

bundle_dir = "~/Library/Application Support/Alfred 2/Workflow Data/cow.pw.convert-currency/"
bundle_dir = os.path.expanduser(bundle_dir)
if not os.path.isdir(bundle_dir):
    os.mkdir(bundle_dir)
pickle_path = bundle_dir + 'convertion_rates.pickle'

changed_currency_dict = False

try:
    with open(pickle_path, 'r') as f:
        currency_dict = pickle.load(f)
except:
    currency_dict = {}
gconvert_pattern = "http://www.google.com/finance/converter?a=${amount}&from={from_currency}&to={to_currency}"


def get_convertion_rate(from_currency, to_currency):
    if from_currency == to_currency:
        return 1., ""
    if not from_currency or not to_currency:
        return 0., "currency not specified"
    try:
        result_html = urllib2.urlopen(
            gconvert_pattern.format(
                amount=1,
                from_currency=from_currency,
                to_currency=to_currency,
            ),
            timeout=timeout
        ).read()
        convertion_rate = float(
            result_html
            .split("<span class=bld>")[1]
            .split(" ")[0]
        )
        currency_dict[(from_currency, to_currency)] = convertion_rate
        global changed_currency_dict
        changed_currency_dict = True
        description = ""
    except:
        if (from_currency, to_currency) in currency_dict:
            convertion_rate = currency_dict[(from_currency, to_currency)]
            description = "OFFLINE"
        else:
            convertion_rate = 0.
            description = "NOT AVAILABLE"
    return convertion_rate, description


# use all caps when adding words or something
symbols = {
    "£": "GBP",
    "$": "USD",
    "€": "EUR",
}


def parse_query(query):
    for symbol in symbols:
        query = query.replace(symbol, " " + symbols[symbol])
    query = query.strip().upper()
    splitted = query.split(" ")
    splitted = [s for s in splitted if s]
    amount = 1.
    from_currency = default_currency
    to_currency = None
    if len(splitted) > 0:
        amount = float(splitted[0])
    if len(splitted) > 1:
        from_currency = splitted[1]
    if len(splitted) > 2:
        to_currency = splitted[-1]
    return (amount, from_currency, to_currency)

icons = {
    "USD": "icons/USD.png",
    "PLN": "icons/PLN.png",
    "EUR": "icons/EUR.png",
    "GBP": "icons/GBP.png",
    "JPY": "icons/JPY.png",
}


def xml(query):
    query = query.upper()
    amount, from_currency, to_currency = parse_query(query)

    currencies = fileslist.to_list()
    if to_currency:
        currencies = [to_currency] + currencies

    al = AlfredItemsList()
    for to_currency in currencies:
        if to_currency == from_currency:
            continue
        convertion_rate, description = get_convertion_rate(from_currency, to_currency)
        converted_amount = str(amount * convertion_rate) + " " + to_currency
        al.append(
            converted_amount,
            converted_amount,
            description,
            icon=icons.get(to_currency, "icons/gen.png")
        )
    return al


if __name__ == "__main__":
    query = " ".join(sys.argv[1:])
    amount, from_currency, to_currency = parse_query(query)

    currencies = fileslist.to_list()
    if to_currency:
        currencies = [to_currency] + currencies
    for to_currency in currencies:
        if to_currency == from_currency:
            continue
        convertion_rate, description = get_convertion_rate(from_currency, to_currency)
        converted_amount = amount * convertion_rate
        print str(converted_amount) + " " + to_currency, description


def save_dict():
    if changed_currency_dict:
        with open(pickle_path, 'w') as f:
            pickle.dump(currency_dict, f)

import atexit
atexit.register(save_dict)
