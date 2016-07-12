#!/usr/bin/env python3
"""Test for config in logalyzer."""

import unittest
import tempfile
import logalyzer


class TesterConfig(unittest.TestCase):
    """Test the config class in logalyzer."""
    # rename the file that this unittest is in.

    config_text = (
        """
        file_name: /home/jade/github/data/data.logfile
        email_to: jadeh@simiya.com
        email_from: noreply@colovore.com
        ignore:
            - DOT11-4-CCMP_REPLAY
            - SNMP-3-AUTHFAIL
            - PARSER-5-CFGLOG_LOGGEDCMD
            - SYS-5-CONFIG_I
        ip_addr: 127.0.0.1
        """)

    # Create temp directory
    file_handle = tempfile.NamedTemporaryFile(delete=False)
    # Write config_text to file in directory
    with open(file_handle.name, 'w+') as another_handle:
        another_handle.write(config_text)

    # Use the name for the file as the file for instantiating configuration
    good_config_file = file_handle
    # name config in the logalyzer code: saves space.
    configuration = logalyzer.Config(good_config_file)

    def test_email_to(self):
        """Test for correct email for reciever.

        Retruns:
            reciever email
         """
        result = self.configuration.email_to()
        self.assertEqual(result, 'jadeh@simiya.com')
        self.assertNotEqual(result, 'bogus@simiya.com')
        self.assertIsInstance(result, str)

    def test_email_from(self):
        """Test for correct email for sender.

        Returns:
            sender email
        """
        result = self.configuration.email_from()
        self.assertEqual(result, 'noreply@colovore.com')
        self.assertNotEqual(result, 'bogus@simiya.com')
        self.assertIsInstance(result, str)

    def test_ignore(self):
        """Test for the right ignore lines.

        Returns:
            if a line with a string in strings is found returns True
        """
        result = self.configuration.ignore()
        # list of ignore phrases in the code to test
        strings = [
            'DOT11-4-CCMP_REPLAY',
            'SNMP-3-AUTHFAIL',
            'PARSER-5-CFGLOG_LOGGEDCMD',
            'SYS-5-CONFIG_I']
        # if a value in strings is found returns True
        for string in strings:
            self.assertEqual(string in result, True)
        self.assertNotEqual(result, 'LINK-3-DOWN')

    def test_file_name(self):
        """Make sure file used is the right data file.

        Returns:
            File which data is retrieved from
        """
        result = self.configuration.file_name()
        self.assertEqual(result, '/home/jade/github/data/data.logfile')
        self.assertNotEqual(result, 'home/jade/github/sata/sata.logfile')
        self.assertIsInstance(result, str)

    def test_ip_addr(self):
        """Make sure ip addresses are found.

        Results:
            ip address that is a string
        """
        result = self.configuration.ip_addr()
        self.assertEqual(result, '127.0.0.1')
        self.assertNotEqual(result, '156.0.0.1')
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
