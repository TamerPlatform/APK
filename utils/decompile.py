import os
import shlex
import subprocess
import shutil

from term_print import print_success, print_err

a2j_url = "https://github.com/AndroidTamer/apk2java"

class APKDecompiler:
    def __init__(self, apk_path):
        if os.path.isabs(apk_path):
            self.apk_path = apk_path
        else:
            self.apk_path = os.path.abspath(apk_path)

    def decompile(self, destination):
        exit_code = os.system("type apk2java >/dev/null 2>&1")
        if exit_code != 0:
            print_err("[-] apk2java doesn't exist! Please install from: %s." % a2j_url)
            return

        if not os.path.exists(self.apk_path):
            print_err("[-] The APK file does not exist.")
            return
      
        print "[*] Proceeding now."

        if not destination:
            print "Using current directory as destination"
            destination = os.getcwd()

        if not destination.startswith("/"): # The path is not absolute, os.path.isabs checks the same thing.
            destination = os.path.abspath(destination)


        if not os.path.isdir(destination):
            print_err("[-] Destination does not exists. Exiting.")
            return

        log_file_name = ".".join([os.path.basename(self.apk_path), "log"])
        log_file_path = os.path.join(destination, log_file_name)
        print "[*] Log file path: {}.".format(log_file_path)

        with open(log_file_path, "w") as out:
            command = shlex.split("apk2java {} {}".format(self.apk_path, destination))
            process = subprocess.Popen(command, stdout=out, stderr=out)
            print "[*] Waiting for apk2java to finish."
            process.wait()


        expected_dir_name = "_".join([self.apk_path, "src"])
        expected_dir_path = os.path.join(destination, expected_dir_name)

        if not os.path.exists(expected_dir_path):
            print_err("[-] Some error occured. Can't find source. Check logs - {}.".format(log_file_path))
        else:
            print_success("[+] Please find the source here: {}".format(expected_dir_path))