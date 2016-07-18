#!/usr/bin/env python3
"""This is a logalyzer script."""

import argparse
from pprint import pprint
import os
from os import stat
from os.path import abspath
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import time
from stat import ST_SIZE
import netifaces
import yaml


class Config(object):
    """Reads information from the data file."""

    def __init__(self, file_name):
        """Create dictionary called self.data to input yaml into.

        Argument:
            file_name: name of file data is coming from

        Returns:
            A dictionary mapping data to the
        """
        with open(file_name, "r") as f_handle:
            self.data = yaml.safe_load(f_handle)
        # pprint(self.data)

    def email_to(self):
        """Obtain reciever email.

        Retrieves the email_to string that is in self.data.

        Returns:
            A str corresponding with email_to

            Example:
                to@gmail.com
        """
        return self.data['email_to']

    def email_from(self):
        """Obtain sender email.

        Retrieves the email_from string that is in self.data.

        Returns:
            A str corresponding with email_from

            Example:
                from@gmail.com
        """
        return self.data['email_from']

    def ignore(self):
        """Ignore lines of data that are irrelevent to needed data.

        Retrieves the ignore strings that are irrelevant to data that
        is needed to be sent in the emails of updates.

        Returns:
            1. None (no key strings for ignore were found)
            2. A string containing the ignore keywords (keys found)
        """
        result = None
        if 'ignore' in self.data:
            result = self.data['ignore']
        return result

    def file_name(self):
        """Name of file that data is coming from.

        Retrieves the file name from self.data on what the data is
        coming from.

        Returns:
            the name of file from file_name in self.data.
        """
        return self.data['file_name']

    def ip_addr(self):
        """Ip address method to record ip addresses.

        TODO: emails are only sent to one ip address once
            sees that the same ip address

        Retrieves an ip address from the self.data file, used to see
        if that ip address is present from device.

        Returns:
            ip address from self.data
        """
        return self.data['ip_addr']


class ReadLine(object):
    """Classify ReadLine so that lines of code are read."""

    def __init__(self, line, config):
        """Define line and config.

        Arguments:
            line: line of code
            config: data from data file
        """
        self.line = line
        self.config = config

    def overlook(self):
        """If a string from self.ignore is seen, the line is disregarded.

        Returns:
            1. keywords are not seen; returns False
            2. keywords are seen; returns True
        """
        found = False
        # if the values in ignore are found; found = True
        for value in self.config.ignore():
            if value in self.line:
                found = True
                break
        return found

    def email(self, test=False):
        """Line that is relevant is found and email is sent.

        Arguments:
            test=False: this is a variable for testing from unittests

        Returns:
            email is sent off of the data that is relevant
            through the server with the text, reciever and sender info
        """
        # define values for sender, reciever, date and message
        email_to = self.config.email_to()
        email_from = self.config.email_from()
        # date is formated as weekday, month, day, year
        date = datetime.datetime.now()
        date.strftime('%b %d %Y')
        msg = MIMEMultipart()
        # header of the email
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = ('Log Activity Alert: %s') % (date)
        subject = msg['Subject']

        # Create the body of the email and attach to message
        body = self.line
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()

        # If not unittesting, send email normally
        if test is False:
            server = smtplib.SMTP('localhost')
            server.sendmail(email_from, [email_to], text)
            server.quit()
        else:
            # Return tuple of data otherwise
            return (email_to, email_from)
        # print('boo')


class LogTail(object):
    """Code is continuously taking data and sending update emails."""

    def __init__(self, config):
        """Define the variables and find the length of file.

        Arguments:
            config: used to see if there are updates in file self.data

        File is opened to see contents and the length is recorded.
        handle reads lines of code one at a time.
        """
        self.config = config
        self.log_file = abspath(config.file_name())
        self.f_handle = open(self.log_file, "r")
        # Find length of the file
        file_len = stat(self.log_file)[ST_SIZE]
        # find the last line of code (current position)
        self.f_handle.seek(file_len)
        self.pos = self.f_handle.tell()

    def _reset(self):
        """Code has variables to be able to continuously reset."""
        self.f_handle.close()
        # open data file
        self.f_handle = open(self.log_file, "r")
        # creat object for position of last line
        self.pos = self.f_handle.tell()

    def tail(self):
        """Tail the file with truncate.

        Returns:
            sent email
        """
        print('Starting Tail')
        while 1:
            # find the last line of code in the data file.
            self.pos = self.f_handle.tell()
            line = self.f_handle.readline()

            if not line:
                # if size of file is less than the position reset code
                if stat(self.log_file)[ST_SIZE] < self.pos:
                    self._reset()

                # if file is greater than position, rest for one minute
                # then find the position of the last line again.
                else:
                    time.sleep(1)
                    self.f_handle.seek(self.pos)
            # if there is a line then read it
            else:
                query = ReadLine(line, self.config)
                # if ignore keywords are not in line then continue
                if query.overlook() is False:
                    # if line does not have ignore keywords; query.email()
                    print('Hooray')


def ip_addresses():
    """Find the IP addresses of the divices that look at file.

    TODO: Make code so that when any divice is looking for data
        logalyzer can find ip address and email to device, if the
        ip address is seen multiple times then anotheremail is not
        sent to device.

    Returns:
        ip_list: the list with the ip addresses
    """
    # list for ip addresses
    ip_list = []

    # Interate over available interfaces
    for interface in netifaces.interfaces():
        # Ignore interfaces with no data
        if bool(netifaces.ifaddresses(interface)) is False:
            continue

        # IPv4 addresses ALWAYS have a key of netifaces.AF_INET (2)
        # Make sure this is the case for this interface
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            # Hooray we have an IPv4 address! Add it to the list
            for interface_data in netifaces.ifaddresses(
                    interface)[netifaces.AF_INET]:
                ip_list.append(interface_data['addr'])

    # Return
    return ip_list


def main():
    """Run main function.

    Returns:
        1.confirmation of verbose turning on
        2.if file name entered is not correct new file name is promted for
        3.tailed data file
    """
    # Create parser object
    parser = argparse.ArgumentParser()

    # Add command line options to expect
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")

    parser.add_argument(
        "-f", "--config_file",
        help="Configration file to process",
        required=True)

    # Make object process all command line options
    args = parser.parse_args()

    # Verify whether CLI option was used
    if args.verbose:
        print("verbosity turned on")

    if os.path.isfile(args.config_file) is False:
        output = ('Filename "%s" does not exist') % (args.config_file)
        print(output)
        sys.exit(0)

    # Rename args.config_file so that it is shorter
    configuration = Config(args.config_file)

    a_list = ip_addresses()
    # If the ip address is in ip_addesses() then tail
    if configuration.ip_addr() in a_list:
        tail = LogTail(configuration)
        tail.tail()

    # print(ip_addresses())
    sys.exit(0)

if __name__ == "__main__":
    main()
