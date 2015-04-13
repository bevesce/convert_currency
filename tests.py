import unittest
import convertcurrency as cc


class ParsingTestCase(unittest.TestCase):
    def setUp(self):
        self.default_from = ('PLN', )
        self.default_to = ('GBP', 'USD')
        self.default_amount = 13
        cc.set_default_currencies_to_convert_from('pln')
        cc.set_default_currencies_to_convert_to('gbp', 'usd')
        cc.set_default_ammount(13)

    def test_amount(self):
        cconv = cc.parse_input('1 PLN GBP')
        self.assertEqual(cconv.amount, 1)
        cconv = cc.parse_input('100.25')
        self.assertEqual(cconv.amount, 100.25)

    def test_defaults(self):
        cconv = cc.parse_input('')
        self.assertEqual(cconv.amount, self.default_amount)
        self.assertEqual(cconv.to_convert_from, self.default_from)
        self.assertEqual(cconv.to_convert_to, self.default_to)

    def test_one_currency(self):
        cconv = cc.parse_input('100 eur')
        self.assertEqual(cconv.to_convert_from, ('EUR', ))
        self.assertEqual(cconv.to_convert_to, self.default_to)

    def test_two_currencies(self):
        cconv = cc.parse_input('100 eur gbp')
        self.assertEqual(cconv.to_convert_from, ('EUR', ))
        self.assertEqual(cconv.to_convert_to, ('GBP', ))

    def test_three_currencies(self):
        cconv = cc.parse_input('100 eur gbp jpy')
        self.assertEqual(cconv.to_convert_from, ('EUR', ))
        self.assertEqual(cconv.to_convert_to, ('GBP', 'JPY'))

    def test_1_in_2(self):
        cconv = cc.parse_input('100 eur in gbp jpy')
        self.assertEqual(cconv.to_convert_from, ('EUR', ))
        self.assertEqual(cconv.to_convert_to, ('GBP', 'JPY'))

    def test_2_in_1(self):
        cconv = cc.parse_input('100 eur gbp in jpy')
        self.assertEqual(cconv.to_convert_from, ('EUR', 'GBP'))
        self.assertEqual(cconv.to_convert_to, ('JPY', ))

    def test_alternative_separator(self):
        cconv = cc.parse_input('100 eur gbp > jpy')
        self.assertEqual(cconv.to_convert_from, ('EUR', 'GBP'))
        self.assertEqual(cconv.to_convert_to, ('JPY', ))


class ConvertTestCase(unittest.TestCase):
    def test_converters_creation(self):
        cconv = cc.parse_input('100 eur in pln gbp')
        converters = tuple(cc.create_conversions(cconv))
        self.assertEqual(len(converters), 2)
        eur_pln_converter = converters[0]
        self.assertEqual(eur_pln_converter.currency_from, 'EUR')
        self.assertEqual(eur_pln_converter.currency_to, 'PLN')
        self.assertEqual(eur_pln_converter.amount, 100)
        eur_gbp_converter = converters[1]
        self.assertEqual(eur_gbp_converter.currency_from, 'EUR')
        self.assertEqual(eur_gbp_converter.currency_to, 'GBP')
        self.assertEqual(eur_gbp_converter.amount, 100)

    def test_online_conversion(self):
        cconv = cc.parse_input('100 eur in pln')
        converter = tuple(cc.create_conversions(cconv))[0]
        self.assertTrue(isinstance(converter.converted_amount, float))

unittest.main()
