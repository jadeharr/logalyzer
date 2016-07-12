#!/usr/bin/env python3
"""Test for ip_addressess in logalyzer."""

import unittest
import logalyzer


class TesterLogTail(unittest.TestCase):
    """Test if logtail is efficient."""
    # rename the file that this unittest is in.
    good_config_file = '/home/jade/github/logalyzer/test/etc/good.yaml'
    # name the test of config in the logalyzer code: lines shorter.
    configuration = logalyzer.Config(good_config_file)

    def test_ip_addresses(self):
        """Test for correct ip address from data file.

        Returns:
            ip address
        """
        result = self.configuration.ip_addr()
        self.assertEqual(result, '127.0.0.1')
        self.assertNotEqual(result, '156.0.0.1')


if __name__ == '__main__':
    unittest.main()
