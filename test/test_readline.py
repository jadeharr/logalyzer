#!/usr/bin/env python3

import unittest
import logalyzer

class Tester(unittest.TestCase):
    """Test the ReadLine class to logalyzer."""
    # rename the file that this unittest is in.
    good_config_file = '/home/jade/github/logalyzer/test/etc/good.yaml'
    # name the test of config in the logalyzer code: lines shorter.
    configuration = logalyzer.Config(good_config_file)

    def test_overlook(self):
        result = self.configuration.ignore()
        strings = ['DOT11-4-CCMP_REPLAY',
            'SNMP-3-AUTHFAIL',
            'PARSER-5-CFGLOG_LOGGEDCMD',
            'SYS-5-CONFIG_I']
        found = False
        for string in strings:
            if string in 'data/data.logfile':
                found = True
                self.assertTrue(string in result, True)

    def test_email(self):
        if test_overlook() == False
            self.assertEqual(test_email, False)

if __name__ == '__main__':
    unittest.main()
