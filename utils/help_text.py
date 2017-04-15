import sys

script = {"name": sys.argv[0]}

download_help = """This command can be used to download APKs from either a device or from the Playstore.

Usage: python {name} -download <APP_ID> <Source> <Optional Destination>

Source could be either "playstore" or "device".

In case source is playstore, the code would search Play Store for given string,
and if it cannot find the app, itwould present you with the search result. 
You can then re-run the code with correct APP_ID.

In case source is device, the code would search in device with given string,
and then prompt user for choosing available apps.

If destination is not provided, file is downloaded in current directory.

Examples: 
python {name} -download com.whatsapp playstore
python {name} -download com.whatsapp playstore /tmp/whatsapp.apk
python {name} -download com.whatsapp playstore /tmp/

""".format(**script)

decompile_help = """This command can be used to decompile APKs using apk2java.
If apk2java is not installed, please visit - https://github.com/AndroidTamer/apk2java.
Please, make sure your apk2java version >= 0.2.
Check your version using: `sudo apt-cache show apk2java | grep Version`

Usage: python {name} -decompile <APK Path> <Optional Destination>

In case DESTINATION path is not provided, the APK would be decompiled in current directory.

Example: 
python {name} -decompile com.whatsapp.apk /tmp/apk_src/
""".format(**script)

sign_help = """This command can be used to sign your APKs using `apksigner`.
The tool expects the keystore to be stored at "~/.apk/keystore.jks". If the tool 
cannot find the keystore there, it would ask you to either specify full path to 
keystore or let the script generate one for you.

Usage: python {name} -sign <APK Path>

If signing is successful, the apk is stored as $apk_name-aligned.apk in same path
as the APK. For example, signing an APK "/tmp/test.apk", the script would sign the
APK and store it as "/tmp/test-aligned.apk"

Example: python {name} -sign com.appname.apk

""".format(**script)