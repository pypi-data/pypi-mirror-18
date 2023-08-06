import unittest

from htop import HTop
from mock import patch


class HTopTest(unittest.TestCase):

    @patch('htop.HTop.get_hdd_stat')
    def test_print_all(self, mocked_funct):
        htop = HTop
        htop.print_all_statistic()
        mocked_funct.assert_called_once()