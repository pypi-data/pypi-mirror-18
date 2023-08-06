import unittest
from ubersmith_client import _http_utils


class HttpUtilsTest(unittest.TestCase):
    def test_form_encode_with_list(self):
        result = _http_utils.form_encode(dict(test=['a', 'b']))
        self.assertDictEqual({
            'test[0]': 'a',
            'test[1]': 'b',
        }, result)

    def test_with_tuples(self):
        result = _http_utils.form_encode(dict(test=('a', 'b')))

        self.assertDictEqual({
            'test[0]': 'a',
            'test[1]': 'b',
        }, result)

    def test_with_dict(self):
        result = _http_utils.form_encode(dict(test={'a': '1', 'b': '2'}))

        self.assertDictEqual({
            'test[a]': '1',
            'test[b]': '2'
        }, result)

    def test_with_empty_dict(self):
        result = _http_utils.form_encode(dict(test_dict={}, test_list=[]))

        self.assertDictEqual({
            'test_dict': {},
            'test_list': []
        }, result)

    def test_with_nested_lists_and_dicts(self):
        result = _http_utils.form_encode(dict(test=[['a', 'b'], {'c': '1', 'd': '2'}]))

        self.assertDictEqual({
            'test[0][0]': 'a',
            'test[0][1]': 'b',
            'test[1][c]': '1',
            'test[1][d]': '2'
        }, result)

    def test_with_bools(self):
        result = _http_utils.form_encode(dict(true=True, false=False))

        self.assertDictEqual({
            'true': True,
            'false': False
        }, result)


