#!/usr/bin/env python3

import unittest
import logalyzer

class Tester(unittest.TestCase):
    """Test for if logtail is efficient."""
    # rename the file that this unittest is in.
    good_config_file = '/home/jade/github/logalyzer/test/etc/good.yaml'
    # name the test of config in the logalyzer code: lines shorter.
    configuration = logalyzer.Config(good_config_file)

    def test_ip_addresses(self):
        result = self.configuration.ip_addr()
        self.assertEqual(result, '127.0.0.1')
        self.assertNotEqual(result, '156.0.0.1')


if __name__ == '__main__':
    unittest.main()
