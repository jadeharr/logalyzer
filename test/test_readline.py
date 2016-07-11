#!/usr/bin/env python3
"""Test for readline in logalyzer."""

import unittest
import logalyzer


class TesterReadLine(unittest.TestCase):
    """Test the ReadLine class to logalyzer."""
    # rename the file that this unittest is in.
    good_config_file = '/home/jade/github/logalyzer/test/etc/good.yaml'
    # name the test of config in the logalyzer code: lines shorter.
    configuration = logalyzer.Config(good_config_file)

    # Create test lines
    line_valid = 'DOT11-4-CCMP_REPLAY blah blah blah'
    line_invalid = 'INVALID-4-STRING blah blah blah'

    # Create object for valid line
    object_valid = ReadLine(line_valid, configuration)
    object_invalid = ReadLine(line_invalid, configuration)

    def test_overlook(self):
        """Test for the ignore values of the code

        Returns:
            False
        """
        # Test with an object instantiated with a valid string
        result = self.object_valid.overlook()
        self.assertEqual(result, False)

        # Test with an object instantiated with an invalid string
        result = self.object_invalid.overlook()
        self.assertEqual(result, True)

        # Create a list of valid lines to test
        strings = [
            'DOT11-4-CCMP_REPLAY',
            'SNMP-3-AUTHFAIL',
            'PARSER-5-CFGLOG_LOGGEDCMD',
            'SYS-5-CONFIG_I']
        for string in strings:
            # Create new object
            new_object = ReadLine(self.configuration, string)
            result = new_object.overlook()
            self.assertEqual(result, False)

    def test_email(self):
        """Test for the header contens in the email

        Returns:
            1. sender email address
            2. reciever email address
        """
        # this test will always be true to test the contents of email
        if test_email() is True:
            # define header contents
            email_to = 'jadeh@simiya.com'
            email_from = 'noreply@gmail.com'

            # test for the header contents to be true
            result = self.email_to.email()
            self.assertEqual(result, True)

            result = self.email_from.email()
            self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main()
