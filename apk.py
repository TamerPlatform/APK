#!/usr/bin/env python2

import os
import argparse
import sys

from utils.download import APKDownloader
from utils.decompile import APKDecompiler
from utils.apksigner import APKSigner
from utils.help_text import download_help, \
                        decompile_help, sign_help

def main():
    if args.download:
        if len(sys.argv) < 4:
            print download_help
            return

        apk_name, source = sys.argv[2], sys.argv[3]
        try: dest = sys.argv[4]
        except IndexError: dest = None
        apk = APKDownloader(apk_name, source)
        apk.download(dest)

    elif args.decompile:
        if len(sys.argv) < 3:
            print decompile_help
            return

        apk_path = sys.argv[2]
        try: dest = sys.argv[3]
        except IndexError: dest = None

        dec = APKDecompiler(apk_path)
        dec.decompile(dest)

    elif args.sign:
        if len(sys.argv) < 3:
            # print "[-] Please specify APK name to sign and zipalign."
            print sign_help
            return

        apk_path = sys.argv[2]
        signer = APKSigner(apk_path)
        signer.sign()





if __name__ == '__main__':
    home_dir = os.path.expanduser("~")
    tool_dir = os.path.join(home_dir, ".apk/")

    # Checking if ~/.apk exists or not. Creating if not.
    if not os.path.isdir(tool_dir):
        print "[*] Work directory does not exist. Creating for you."
        os.mkdir(tool_dir)

    # Checking if gplaycreds.conf exists or not. Create with random content, if not.
    creds_file = os.path.join(tool_dir, "gplaycreds.conf")
    if not os.path.isfile(creds_file):
        print "[*] Google play creds file does not exist. Creating one for you."
        print "[*] Please, edit the file. See README.md for format."
        with open(creds_file, "w") as fh:
            fh.write("# Please edit this file")

    description = """Wrapper for various APK commands.
    For detailed usage of a command, simply run the command with no argument.

    Example: python {} -download
    """.format(sys.argv[0])

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-download',
                        help="Download an APK from either the playstore or device.",
                        action="store_true")
    parser.add_argument('-decompile',
                        action="store_true",
                        help='Decompile the given APK using apk2java.')
    parser.add_argument('-sign',
                        action="store_true",
                        help='Zipalign\'s and Signs the given APK.')
    
    args, unknown = parser.parse_known_args()

    if not (args.download or args.decompile or args.sign):
        parser.print_usage()
        parser.exit(1)
    main()