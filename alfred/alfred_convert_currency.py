import sys
from alfred import AlfredItemsList
from convert_currency import convert_currency


def convert(query):
    al = AlfredItemsList()
    try:
        for amount, currency in convert_currency(query):
            al.append(
                arg='{:.2f}'.format(amount),
                title='{:.2f} {}'.format(amount, currency),
                subtitle='',
            )
    except Exception as e:
        al.append('error', 'Error', str(e))
    print(al)


convert(' '.join(sys.argv[1:]))
