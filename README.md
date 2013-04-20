# Convert currency

Alfred workflow and python script that converts currencies using [https://www.google.com/finance/converter]()

Converter works offline, when there is no internet connection currency exchange rate from the last time when script/workflow were used to convert given pair of currencies.

## Usage

Just type the argument:

- 10 usd in jpy - displays yen and favorite currencies

![10 usd in jpy][cc1]

- 10$€ - displays euro and favorite currencies
- 10 usd - displays favorite currencies 

![10 usd][cc2]

- 10 - uses default currency - can be specified in *convertcurrency.py*
- *no argument* - uses default currency and 1 as amount

![1 pln][cc3]

## Workflow

- Tapping *return* ↩ in workflow pastes result of conversion to active application.
- Tapping *command+return* ⌘+↩ marks currency as favorite - it will be automatically displayed always when converter works.

[cc1]: http://bvsc.nazwa.pl/img/convertcurrency1.png
[cc2]: http://bvsc.nazwa.pl/img/convertcurrency2.png
[cc3]: http://bvsc.nazwa.pl/img/convertcurrency3.png
