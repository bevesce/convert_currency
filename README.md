# Convert Currency

Alfred workflow and python script that converts currencies using [http://www.google.com/finance/converter](http://www.google.com/finance/converter)

![alfred workflow](http://procrastinationlog.net/images/convert-currency.png)

## Usage

Set this two variables in *convertcurrency.py*:
```
    DEFAULT_CURRENCIES_TO_CONVERT_FROM = ('EUR', 'USD')
    DEFAULT_CURRENCIES_TO_CONVERT_TO = ('PLN', )
```

And then just pass argument that looks something like one of those examples:

* 10
* 10 gbp
* 10 gbp eur
* 10 gbp eur usd
* 10 pln in eur usd
* 10 pln eur in usd
* 10 pln eur > usd