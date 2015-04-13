from alfredlist import AlfredItemsList
from convertcurrency import convert_currency


def convert(text):
    al = AlfredItemsList()
    for conversion in convert_currency(text):
        al.append(unicode(conversion.converted_amount), unicode(conversion), '')
    print al
