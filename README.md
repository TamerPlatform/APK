# APK

### Introduction

This project aims to be a single place for APK related operations. That also explains the unoriginal name for the project: APK. This project was written to solve this [Android Tamer requirement](https://github.com/AndroidTamer/Tools_Repository/issues/41). As of now, following operations are supported:

- Download APKs from
    - Playstore (Google account credentials required)
    - Device (Should be connected via adb)
- Decompiling an APK
- Zipalign-ing and signing an APK


### Requirements
- Linux based OS (Tested on Android Tamer)
- Python 2.7
- [apk2java](https://github.com/AndroidTamer/apk2java)
- apksigner (Android SDK build tools >= 24.0.3)
- zipalign (Android SDK build tools)
- adb (Android SDK tools)
- keytool 
- pip (use requirements.txt)
    - protobuf
    - clint
    - requests


### Setting up:

1. Make sure that all the requirements are met. To install Python libraries, run
```bash
pip install -r requirements.txt
```
2. Run the code first time to create necessary files:
```bash
python apk.py
```

3. Edit the credentials file (`~/.apk/gplaycreds.conf`):
```bash
[Credentials]
gmail_password = password # Your Google account password
android_ID = 3d716411bf8bc802 # Or your own Android Device ID
gmail_address = xyz@gmail.com # Your Google account Email
language = en_US 
```

4. If you already have a keystore, move it to `~/.apk/` as `keystore.jks`. If you don't have one, the code will create for you when you use "-sign" option.
```bash
cp <path to your keystore> ~/.apk/keystore.jks
```

### Usage:

To see the available options, run:
```bash
python apk.py --help

# Output below
usage: apk.py [-h] [-download] [-decompile] [-sign]

Wrapper for various APK commands. For detailed usage of a command, simply run
the command with no argument. Example: python apk.py -download

optional arguments:
  -h, --help  show this help message and exit
  -download   Download an APK from either the playstore or device.
  -decompile  Decompile the given APK using apk2java.
  -sign       Zipalign's and Signs the given APK.
```

To see the help for any specific command, run the command with no arguments. Example:
```bash
$ python apk.py -download

# Output below
This command can be used to download APKs from either a device or from the Playstore.

Usage: python apk.py -download <APP_ID> <Source> <Optional Destination>

Source could be either "playstore" or "device".

In case source is playstore, the code would search Play Store for given string,
and if it cannot find the app, itwould present you with the search result. 
You can then re-run the code with correct APP_ID.

In case source is device, the code would search in device with given string,
and then prompt user for choosing available apps.

If destination is not provided, file is downloaded in current directory.

Examples: 
python apk.py -download com.whatsapp playstore
python apk.py -download com.whatsapp playstore /tmp/whatsapp.apk
python apk.py -download com.whatsapp playstore /tmp/

```

Similar can be used for other commands as,
```bash
$ python apk.py -decompile
$ python apk.py -sign
```

### To do list
- Code documentation
- APK security scan (?)