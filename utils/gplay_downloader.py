#! /usr/bin/python2
# -*- coding: utf-8 -*-
""" This code is a modified version of GPlay-Cli by Matlink.
This code is used by Android Tamer project for downloading APKs.
Original docstring below:

GPlay-Cli
Copyleft (C) 2015 Matlink
Hardly based on GooglePlayDownloader https://codingteam.net/project/googleplaydownloader
Copyright (C) 2013   Tuxicoman

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not,
see <http://www.gnu.org/licenses/>.
"""

import os
import ConfigParser
from ext_libs.googleplay_api.googleplay import GooglePlayAPI  # GooglePlayAPI
from ext_libs.googleplay_api.googleplay import LoginError

from term_print import print_success, print_err

class GPlayDownloader(object):
    def __init__(self):
        # Overide credentials if present in .config
        config_file = os.path.expanduser("~") + '/.apk/gplaycreds.conf'
        if os.path.isfile(config_file):
            self.fail = False
            credentials = config_file
            self.configparser = ConfigParser.ConfigParser()
            self.configparser.read(credentials)
            self.config = dict()
            for key, value in self.configparser.items("Credentials"):
                self.config[key] = value
            self.verbose = True
        else:
            print_err("[-] Config file not found.")
            print "[*] Please put credentials.conf file here: %s" % config_file
            self.fail = True

    def connect_to_googleplay_api(self):
        api = GooglePlayAPI(androidId=self.config["android_id"], lang=self.config["language"])
        error = None
        try:
            api.login(self.config["gmail_address"], self.config["gmail_password"], None)
        except LoginError, exc:
            error = exc.value
            success = False
        else:
            self.playstore_api = api
            success = True
        return success, error

    def sizeof_fmt(self, num):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f%s" % (num, x)
            num /= 1024.0

    def raw_search(self, results_list, search_string, nb_results):
        # Query results
        return self.playstore_api.search(search_string, nb_results=nb_results).doc

    def search(self, results_list, search_string, nb_results, free_only=True, include_headers=True):
        results = self.raw_search(results_list, search_string, nb_results)
        if len(results) > 0:
            results = results[0].child
        else:
            print "No result"
            return
        all_results = list()
        if include_headers:
            # Name of the columns
            col_names = ["Title", "Creator", "Size", "AppID", "Version"]
            all_results.append(col_names)
        # Compute results values
        for result in results:
            if free_only and result.offer[0].checkoutFlowRequired:  # if not Free to download
                continue
            l = [result.title,
                 result.creator,
                 self.sizeof_fmt(result.details.appDetails.installationSize),
                 result.docid,
                 result.details.appDetails.versionCode
                 ]
            all_results.append(l)

        if self.verbose:
            # Print a nice table
            col_width = list()
            for column_indice in range(len(all_results[0])):
                col_length = max([len(u"%s" % row[column_indice]) for row in all_results])
                col_width.append(col_length + 2)

            for result in all_results:
                print "".join((u"%s" % item).encode('utf-8').strip().ljust(col_width[indice]) for indice, item in
                              enumerate(result))
        return all_results

def main():
    print "[-] Please run this as a module."


if __name__ == '__main__':
    main()
