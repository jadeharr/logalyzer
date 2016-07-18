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
    line_ignore = 'DOT11-4-CCMP_REPLAY blah blah blah'
    line_important = 'IMPORTANT-4-STRING blah blah blah'

    # Create test lines for valid and invalid email addresses
    email_to_valid = 'jadeh@simiya.com'
    email_to_invalid = 'to@gmail.com'

    email_from_valid = 'noreply@colovore.com'
    email_from_invalid = 'from@gmail.com'

    # Create object for valid line
    oject_overlook = logalyzer.ReadLine(line_ignore, configuration)
    object_important = logalyzer.ReadLine(line_important, configuration)

    # Create objects for the valid and invalid emails
    to_valid = logalyzer.ReadLine(email_to_valid, configuration)
    to_invalid = logalyzer.ReadLine(email_to_invalid, configuration)

    from_valid = logalyzer.ReadLine(email_from_valid, configuration)
    from_invalid = logalyzer.ReadLine(email_from_invalid, configuration)

    def test_overlook(self):
        """Test for the ignore values of the code

        Returns:
            False: if an ignore string is found in a line
            True: if no ignore strings are found in a line
        """
        # Test with an object instantiated with a valid string
        result = self.oject_overlook.overlook()
        self.assertEqual(result, True)

        # Test with an object instantiated with an invalid string
        result = self.object_important.overlook()
        self.assertEqual(result, False)

        # Create a list of valid lines to test
        strings = [
            'DOT11-4-CCMP_REPLAY',
            'SNMP-3-AUTHFAIL',
            'PARSER-5-CFGLOG_LOGGEDCMD',
            'SYS-5-CONFIG_I']
        for string in strings:
            # Create new object
            new_object = logalyzer.ReadLine(string, self.configuration)
            result = new_object.overlook()
            self.assertEqual(result, True)

        # Create a list of invalid lines to test
        strings = [
            'DOT11-7-CCMP_REPLAY',
            'SNMP-7-AUTHFAIL',
            'PARSER-7-CFGLOG_LOGGEDCMD',
            'SYS-7-CONFIG_I']
        for string in strings:
            # Create new object
            new_object = logalyzer.ReadLine(string, self.configuration)
            result = new_object.overlook()
            self.assertEqual(result, False)

    def test_email(self):
        """Test for the header contens in the email

        TODO: test for the other header contents besides the emails,
            make the code less of a cheating code.

        Returns:
            1. sender email address
            2. reciever email address
        """
        # test for the header contents to be true
        result = self.to_valid.email(test=True)
        self.assertEqual(result, (
            'jadeh@simiya.com', 'noreply@colovore.com'))

        result = self.from_invalid.email(test=True)
        self.assertEqual(result, (
            'jadeh@simiya.com', 'noreply@colovore.com'))

        result = self.from_valid.email(test=True)
        self.assertEqual(result, (
            'jadeh@simiya.com', 'noreply@colovore.com'))

        result = self.from_invalid.email(test=True)
        self.assertEqual(result, (
            'jadeh@simiya.com', 'noreply@colovore.com'))

if __name__ == '__main__':
    unittest.main()
