import unittest

import plandf

class BasicTest(unittest.TestCase):
    def test_hello_world(self):
        p = plandf.Plan()
        p.steps([
                {'input': 'time: 1; carrots: 2; cucumbers: 3',
                'output': 'liters of juice: 0.5; waste material grams: 20'}
        ])
        self.assertEqual(p.info.df['input']['time'][0],
                         {'f_price': u'',
                           'f_units': '',
                           'max_price': u'',
                           'max_units': '1',
                           'min_price': u'',
                           'min_units': '1',
                           'price_unit': u''})

if __name__ == '__main__':
    unittest.main()
