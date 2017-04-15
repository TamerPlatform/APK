import commands
import os
from ConfigParser import ConfigParser
import shlex
import subprocess
import os
import commands

from term_print import print_success, print_err


"""
1) if ~/.apk/keystore.jks exist use it.
2) if that doesn't exist:
    i. Either generate one for user and store in keystore.jks.
    ii. Or ask user for path to their own keystore.
3) Zipalign the APK.
4) Sign the APK.
"""

keygen_cmd = 'keytool -genkey -v -keystore {} -alias ' \
             '"tamer" -keyalg RSA -keysize 2048 -validity 10000 ' \
             '-dname "CN=Android, OU=Tamer, O=androidtamer.com, ' \
             'L=Bhopal, ST=Madhya Pradesh, C=IN" -keypass android ' \
             '-storepass android'

default_keystore_details = """
Keystore Alias:             tamer
Keystore Password:          android
First Name and Last Name:   Android Tamer
Organization:               androidtamer.com
Organization Unit:          NA
City, State, Country:       Bhopal, Madhya Pradesh, India
"""

sign_cmd = "apksigner sign {} --ks {} {}"
sign_cmd_pass_arg = "--ks-pass pass:android"

class APKSigner:
    def __init__(self, apk_path):
        self.expected_keystore_path = os.path.join(os.path.expanduser("~"), ".apk/keystore.jks")
        if os.path.isfile(apk_path):
            self.error = False
            self.apk_path = apk_path
            if os.path.isabs(apk_path):
                self.apk_path = apk_path
            else:
                self.apk_path = os.path.abspath(apk_path)
            self.signed = False
        else:
            print_err("[-] Couldn't find the specified APK file.")
            self.error = True

        for binary in ["keytool", "jarsigner"]:
            exit = os.system("type {} >/dev/null 2>&1".format(binary))
            if exit != 0:
                print_err("[-] {} does not exists in system path. Please fix!".format(binary))
                self.error = True

    def sign(self):
        if self.error:
            return

        keystore_path = self.expected_keystore_path

        print "[*] The script will use {} by default if it exists.".format(self.expected_keystore_path)
        if not os.path.isfile(self.expected_keystore_path):
            print_err("[-] Default keystore doesn't exist.")
            choice = raw_input("[*] Do you want to create keystore now? (yes/no): ")
            if "yes" in choice.lower():
                if not self._gen_keystore():
                    print_err("[-] Failed to create keystore. Exiting.")
                    return
                print_success("[+] Keystore generated for you.")
            else:
                choice = raw_input("[*] Do you want to specify path to keystore? (yes/no): ")
                if "no" in choice:
                    print_err("[-] No keystore selected. Exiting.")
                    return
                else:
                    user_keystore_path = raw_input("[*] Enter keystore path: ").strip()
                    if not os.path.isfile(user_keystore_path):
                        print_err("[-] Provided keystore file does not exist. Please, check again.")
                        return
                    else:
                        keystore_path = user_keystore_path
        else:
            keystore_path = self.expected_keystore_path

        print "[*] Using keystore store at - {}.".format(keystore_path)
        print "[*] Running zipalign on APK before signing."

        aligned_apk_path = self.zipalign()
        if aligned_apk_path:
            print_success("[+] APK zipalign'ed and saved as - {}".format(aligned_apk_path))
        else:
            print_err("[-] Failed to zipalign APK. Exiting")
            return

        print "[*] Signing APK now."
        success = self._sign(keystore_path, aligned_apk_path)
        if success:
            print_success("[+] APK successfully signed.")
            print_success("[+] Please find the signed APK here: {}".format(aligned_apk_path))
        else:
            print_err("[-] Failed to sign the APK.")

    def _gen_keystore(self):
        print "[*] Creating keystore with following data:"
        print default_keystore_details
        cmd = keygen_cmd.format(self.expected_keystore_path)
        exit = os.system(cmd)
        if exit == 0:
            return True
        return False

    def _sign(self, keystore_path, apk_path):
        if keystore_path == self.expected_keystore_path:
            cmd = sign_cmd.format(sign_cmd_pass_arg, keystore_path, apk_path)
        else:
            # Since we are using user provided cert here, we cannot give password arg
            cmd = sign_cmd.format("", keystore_path, apk_path) 
        exit = os.system(cmd)
        if exit == 0:
            return True
        return False

    def zipalign(self):
        if self.apk_path.endswith(".apk"):
            aligned_apk_path = self.apk_path[0:-4] + "-aligned.apk"
        else:
            aligned_apk_path = self.apk_path + "-aligned.apk"
        command = "zipalign -f 4 {} {}".format(self.apk_path, aligned_apk_path)
        status_code = os.system(command)
        if status_code == 0:
            return aligned_apk_path
        return False