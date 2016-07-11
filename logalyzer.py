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
        with open(file_name) as f_handle:
            self.data = yaml.safe_load(f_handle)
        # pprint(self.data)

    def email_to(self):
        """Have a to email to send emails to once an update is found.

        Retrieves the email_to string that is in self.data.

        Returns:
            A str corresponding with email_to

            Example:
            to@gmail.com
        """
        return self.data['email_to']

    def email_from(self):
        """Need to know who/where the email is coming from.

        Retrieves the email_from string that is in self.data.

        Returns:
            A str corresponding with email_from

            Example:
            noreply@gmail.com
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

        TODO: Add more code so that emails are only sent
            to one ip address once

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

        they are used to see each line of code individually
        and config is used to put files together.

        Returns:

        """
        self.line = line
        self.log_file = config

    def overlook(self):
        """if a string of self.ignore is seen, it is disregarded.

        Returns:
            1. the keywords are not seen then it code continues, returns False
            2. keywords are seen then code breaks and an email is not sent out
        """
        found = False
        for value in self.log_file.ignore():
            if value in self.line:
                found = True
                break
        return found

    def email(self, test = False):
        """Line that is relevant is found and email is sent.

        Reciever, sender and subject are defined, email_to and
        email_from are recieved from the self.data file.

        MIMEMultipart is used to send text in the email
        and is equal to msg to make the code shorter

        MimeText is used to help create the body of the message.

        Sender, recipiant, subject and body are coded as strings.

        Server is used to define SMTP (simple mail transfer protocal)
        using the localhost server, string can be changed to another server

        Returns:
            email is sent off of the data that is relevant
            through the server with the text, reciever and sender info
        """
        email_to = self.log_file.email_to()
        email_from = self.log_file.email_from()
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = "Fluctuations In The Data"

        body = "Line"
        msg.attach(MIMEText(body, 'plain'))

        text = msg.as_string()

        server = smtplib.SMTP('localhost')
        server.sendmail(email_from, [email_to], text)
        server.quit()

        # print('boo')


class LogTail(object):
    """Make sure the code is continuously taking data.

    and sending update emails.
    """

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
        file_len = stat(self.log_file)[ST_SIZE]
        self.f_handle.seek(file_len)
        self.pos = self.f_handle.tell()

    def _reset(self):
        """Make sure the code has variables to continuously reset.

        Open the file that needs to be read and read lines
        of code one at a time, make it equal to the position of the
        last line.
        """
        self.f_handle.close()
        self.f_handle = open(self.log_file, "r")
        self.pos = self.f_handle.tell()

    def tail(self):
        """Tail the the truncate file.

        Find the positon of the last line and read it.

        If there is no line to read at the end of the code
        the code will search for the size of the file.
            1. If it is greater than the position the line it
            is reading is on the fiel will update.
            2. If the size of the file is smaller than the position
            of th line it is reading the code will not run for a minute
            then it startes to look for the position againa fer the
            sleep time.

        If the line at the end of the code can be read,
        it will look for the key ignore strings and if they are not
        present on the line an email will be sent.
        """
        print('Starting Tail')
        while 1:
            self.pos = self.f_handle.tell()
            line = self.f_handle.readline()
            if not line:
                if stat(self.log_file)[ST_SIZE] < self.pos:
                    self._reset()
                else:
                    time.sleep(1)
                    self.f_handle.seek(self.pos)
            else:
                query = ReadLine(line, self.config)
                if query.overlook() is False:
                    # query.email()
                    print('Hooray')


def ip_addresses():
    """Find the IP addresses of the divices that look at file.

    TODO: Make code so that when any divice is looking for data
        logalyzer can find ip address and email to device, if the
        ip address is seen multiple times then anotheremail is not
        sent to device.

    Create list to store ip addresses in.

    For all network interfaces if ip addresses are not found
    the code continues. This is to make sure that the code doesn't
    return an error message for ip addresses.

    If an ip address is found then make sure that the address has
    a key for netifaces.AF_INET, ip from the internet. If this is true
    the ip address is appended to the list.

    Returns:
        ip_list: the list with the ip addresses
    """
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

    Create and object called parser to split aguments
    into chunks from the commandline.

    Command line args:
        Make an argument for verbose in help with the key -v

        Make anoher argument for config_file. The file used to
        process configuration file. use key -f.

    Parser object is used to process the command line arguments
    that were just created.

    If arguments are used then print that it is there.

    If a file name is used that does not exist code explains
    and exits out of the system.

    Rename the args.config_filw using the config class ao that
    the code is not as long and is a litle easier to read.

    If the ip address that is found is in the data file then
    tail the file from LogTail to start sending emails to ip address.
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
