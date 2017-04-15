#!/usr/bin/env python

import os
import subprocess
import shlex
import commands
import re

from term_print import print_success, print_err
from gplay_downloader import GPlayDownloader

class APKDownloader:
    def __init__(self, apk_name, source):
        self.apk_name = apk_name
        self.error = False
        self.source = source

        if self.source not in ["device", "playstore"]:
            self.error = True
            print_err("[-] Specify correct source to download from.")
            print "[*] Valid source options: \"device\" or \"playstore\""

    def download(self, destination):
        if self.error:
            return

        if not destination:
            destination = os.getcwd()

        if self.source == "device":
            self._download_from_device(destination)
        else:
            self._download_from_playstore(destination)

    def _download_from_playstore(self, destination):
        gplay = GPlayDownloader()
        if not gplay.fail:
            success, error = gplay.connect_to_googleplay_api()

            if not success:
                print_err("Cannot login to GooglePlay. {}".format(error))
                return

            data = gplay.playstore_api.details(self.apk_name)
            doc = data.docV2
            vc = doc.details.appDetails.versionCode
            if not doc:
                print_err("[-] Couldn't find details for the APK.")
                return

            if not doc.detailsUrl or not doc.title:
                print_err("[-] No APK found to be downloaded.")
                print "[*] Here's a search result for your query string.\n"
                nb_results = 10
                gplay.search(list(), self.apk_name, nb_results)
                print "\n\n[*] Use the AppID from above result to download desired app."
            else:
                print "[+] Downloading APK: %s." % doc.title
                # Prepare destination path
                destination = self._get_destination_path(destination, self.apk_name)

                data = gplay.playstore_api.download(self.apk_name, vc, progress_bar=True)

                # file_name = destination + "/" + doc.docid + ".apk"
                # if destination.endswith(".apk"):
                #     file_name = destination

                with open(destination, "w") as f:
                    f.write(data)

                print_success("[+] APK file saved here - %s." % destination) 
 

    def _download_from_device(self, destination):
        exit_code, _ = commands.getstatusoutput("type adb >/dev/null 2>&1")
        if exit_code != 0:
            print_err("[-] adb doesn't exist! Please install.")
            return

        command = "adb shell pm list packages | grep -i %s" % self.apk_name
        status, output = commands.getstatusoutput(command)
        if status != 0:
            print_err("[-] Error: adb failed to find packages with given string.")
            print_err("[-] Also check connection with device.")
            return

        apks = {}
        count = 0
        for line in output.split("\n"):
            if line:
                if re.match("^package:", line):
                    apks[count] = re.sub("^package:", "", line)
                    count += 1

        if count == 0:
            print_err("[-] No APK found. Exiting.")
            return

        print "[+] Found %d APK(s) with given string." % count
        print "[*] Please, select from the list below:"
        for i in xrange(count):
            print "\t[%d]: %s" %(i, apks[i])

        while True:
            choice = int(input("[*] Enter a number: "))
            if choice not in range(count):
                print_err("[-] Invalid choice.")
                continue
            break

        full_path_command = "adb shell pm path %s" % apks[choice]
        output = commands.getoutput(full_path_command.strip())
        full_path = re.sub("^package:", "", output)
        print "[+] Pulling package from: %s."  % full_path

        destination = _get_destination_path(destination, apks[choice])

        pull_package_command = "adb pull %s %s" % (full_path.strip(), destination)
        status, output = commands.getstatusoutput(pull_package_command)
        if status == 0:
            print_success("[+] Pulled APK successfully. Find here: %s." % destination)
        else:
            print_err("[-] adb failed to pull package. Output below: ")
            print output

    def _get_destination_path(self, path, apk_name):
        if path.endswith(".apk"):
            dir_name, file_name = os.path.split(path)
        else:
            dir_name, file_name = path, apk_name + ".apk"

        if not dir_name.startswith("/"):
            dir_name = os.path.abspath(dir_name)

        if not os.path.exists(dir_name):
            print_err("[-] Given path does not esists. Trying to create.")
            os.mkdir(dir_name)

        return os.path.join(dir_name, file_name)
