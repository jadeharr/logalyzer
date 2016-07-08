#!/usr/bin/env python3

import unittest
import logalyzer

class Tester(unittest.TestCase):
    """Test the config class in logalyzer."""
    # rename the file that this unittest is in.
    good_config_file = '/home/jade/github/logalyzer/test/etc/good.yaml'
    # name the test of config in the logalyzer code: lines shorter.
    configuration = logalyzer.Config(good_config_file)

    def test_email_to(self):
        """Test email_to to make sure that only one email.

         will work in the code.
        """
        result = self.configuration.email_to()
        self.assertEqual(result, 'jadeh@simiya.com')
        self.assertNotEqual(result, 'bogus@simiya.com')
        self.assertIsInstance(result, str)

    def test_email_from(self):
        """Test email_from to make sure that only one email.

        will work in the code.
        """
        result = self.configuration.email_from()
        self.assertEqual(result, 'noreply@colovore.com')
        self.assertNotEqual(result, 'bogus@simiya.com')
        self.assertIsInstance(result, str)

    def test_ignore(self):
        """Test to make sure that the items.

        that need to be ignores are ignored.
        """
        result = self.configuration.ignore()
        strings = ['DOT11-4-CCMP_REPLAY',
            'SNMP-3-AUTHFAIL',
            'PARSER-5-CFGLOG_LOGGEDCMD',
            'SYS-5-CONFIG_I']
        for string in strings:
            self.assertEqual(string in result, True)
        self.assertNotEqual(result, 'LINK-3-DOWN')

    def test_file_name(self):
        """Test to make sure that the data file for the.

        config information is the only file used.
        """
        result = self.configuration.file_name()
        self.assertEqual(result,'/home/jade/github/data/data.logfile')
        self.assertNotEqual(result, 'home/jade/github/data/sata.logfile')
        self.assertIsInstance(result, str)

    def test_ip_addr(self):
        """This is to make sure that ip addresses are found."""
        result = self.configuration.ip_addr()
        self.assertEqual(result, '127.0.0.1')
        self.assertNotEqual(result, '156.0.0.1')
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
