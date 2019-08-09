#!/usr/bin/env python2

# Add and remove test IPA user accounts
# Uses Python Fire library to generate a CLI for the TestUsers class
# Uses names library to generate random user names

# Run with no arguments for usage help
# Obtain IPA admin Kerberos credentials before running the script


import sys
import os
import fire
import names
from ipalib import api, errors

# Initialize API
api.bootstrap_with_global_options(context='cli')
api.finalize()
api.Backend.rpcclient.connect()


class TestUsers:
    def add(self):
        """Generate and add test users to IPA and append the UIDs to a data file."""
        """Adds 10 users by default, adjust the range maximum to taste."""
        datafile = open('userlist.txt', 'a')
        print
        for i in range(0, 10):
            full_name = names.get_full_name()
            username = full_name.lower().replace(" ", ".")
            first_name = full_name.split()[0]
            last_name = full_name.split()[1]
            print "Adding user: %s" % full_name
            api.Command['user_add'](username, givenname=first_name, sn=last_name)
            datafile.write(username + "\n")

        print "\nComplete.\n"
        api.Backend.rpcclient.disconnect()
        datafile.close()

    def delete(self):
        """Parse data file for list of UIDs and delete them from IPA."""
        print
        try:
            datafile = open('userlist.txt', 'r')
        except IOError:
            print "No data file found...exiting.\n"
            sys.exit()

        for user in datafile:
            try:
                print "Deleting uid: %s" % user,
                unic_user = unicode(user, "utf-8")
                api.Command['user_del'](unic_user)
            except errors.NotFound:
                continue

        print "\nComplete.\n"
        api.Backend.rpcclient.disconnect()
        datafile.close()
        os.remove("userlist.txt")


def main():
    fire.Fire(TestUsers)


if __name__ == '__main__':
    main()
