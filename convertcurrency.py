from collections import namedtuple
import urllib2


DEFAULT_AMOUNT = 1
DEFAULT_CURRENCIES_TO_CONVERT_FROM = ('EUR', 'USD')
DEFAULT_CURRENCIES_TO_CONVERT_TO = ('PLN', )


def set_default_ammount(amount):
    global DEFAULT_AMOUNT
    DEFAULT_AMOUNT = amount


def set_default_currencies_to_convert_from(*args):
    global DEFAULT_CURRENCIES_TO_CONVERT_FROM
    DEFAULT_CURRENCIES_TO_CONVERT_FROM = _make_tuple_of_uppercase(args)


def set_default_currencies_to_convert_to(*args):
    global DEFAULT_CURRENCIES_TO_CONVERT_TO
    DEFAULT_CURRENCIES_TO_CONVERT_TO = _make_tuple_of_uppercase(args)


def _make_tuple_of_uppercase(args):
    return tuple((a.upper() for a in args))


def parse_input(input_text):
    """
    * -> DEFAULT_AMOUNT DEFAULT_CURRENCIES_TO_CONVERT_FROM DEFAULT_CURRENCIES_TO_CONVERT_TO
    * 10 -> 10 DEFAULT_CURRENCIES_TO_CONVERT_FROM DEFAULT_CURRENCIES_TO_CONVERT_TO
    * 10 GBP -> 10 (GBP) DEFAULT_CURRENCIES_TO_CONVERT_TO
    * 10 GBP EUR -> 10 (GBP) (EUR)
    * 10 GBP EUR USD -> 10 (GBP) (EUR, USD)
    * 10 gbp in eur usd -> 10 (GBP) (EUR, USD)
    * 10 gbp eur in usd -> 10 (GBP, USD) (EUR)
    * 10 gbp eur > usd -> 10 (GBP, USD) (EUR)
    """
    currency_to_convert = namedtuple(
        'CurrencyToConvert',
        ['amount', 'to_convert_from', 'to_convert_to']
    )
    splited = _split_to_words(input_text)
    amount = _parse_amount(splited)
    convert_from, convert_to = _split_currencies(splited[1:])
    convert_from = convert_from or DEFAULT_CURRENCIES_TO_CONVERT_FROM
    convert_to = convert_to or DEFAULT_CURRENCIES_TO_CONVERT_TO
    return currency_to_convert(amount, convert_from, convert_to)


def _split_to_words(input_text):
    splited = input_text.upper().replace(',', '').strip().split(' ')
    return [w for w in splited if w]


def _parse_amount(splited):
    return float(splited[0]) if splited else DEFAULT_AMOUNT


def _split_currencies(splited_words):
    if not splited_words:
        return None, None
    if len(splited_words) == 1:
        return _make_tuple_of_uppercase(splited_words), None
    for separator in ('IN', '>'):
        if separator in splited_words:
            return _split_currencies_using_separator(separator, splited_words)
    return _make_tuple_of_uppercase([splited_words[0]]), _make_tuple_of_uppercase(splited_words[1:])


def _split_currencies_using_separator(separator, splited_words):
    separator_index = splited_words.index(separator)
    return (
        _make_tuple_of_uppercase(splited_words[:separator_index]),
        _make_tuple_of_uppercase(splited_words[separator_index + 1:])
    )


class Conversion(object):
    url_template = "http://www.google.com/finance/converter?a={amount}&from={from_currency}&to={to_currency}"

    def __init__(self, amount, currency_from, currency_to):
        self.amount = amount
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.converted_amount = self._convert()

    def _convert(self):
        full_url = self._make_full_url()
        result_html = urllib2.urlopen(full_url).read()
        return self._parse_html(result_html)

    def _make_full_url(self):
        return self.url_template.format(
            amount=self.amount,
            from_currency=self.currency_from,
            to_currency=self.currency_to,
        )

    def _parse_html(self, html):
        try:
            return float(
                html.split("<span class=bld>")[1].split(" ")[0]
            )
        except Exception:
            return None

    def __unicode__(self):
        if self.converted_amount is None:
            return u'conversion error'
        return u'{converted_amount} {to_currency} = {amount} {from_currency}'.format(
            converted_amount=self.converted_amount,
            to_currency=self.currency_to,
            amount=self.amount,
            from_currency=self.currency_from,
        )


def create_conversions(parsed_input):
    for cfrom in parsed_input.to_convert_from:
        for cto in parsed_input.to_convert_to:
            yield Conversion(
                parsed_input.amount,
                currency_from=cfrom,
                currency_to=cto
            )


def convert_currency(input_text):
    parsed_input = parse_input(input_text)
    conversions = create_conversions(parsed_input)
    return conversions


if __name__ == '__main__':
    import sys
    input_text = ' '.join(sys.argv[1:])
    print u'\n'.join((unicode(c) for c in convert_currency(input_text)))
