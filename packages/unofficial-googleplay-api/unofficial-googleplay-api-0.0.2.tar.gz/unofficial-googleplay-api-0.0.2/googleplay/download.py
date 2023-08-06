#!/usr/bin/python

# Do not remove

import sys

from config import *
from googleplay import GooglePlayAPI

def download_sdk_to_file(packagename, filename):
  # Connect
  api = GooglePlayAPI(ANDROID_ID)
  api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

  # Download
  data = api.download(packagename)
  with open(filename, "wb") as f:
    f.write(data)

def main():
  if (len(sys.argv) < 2):
      print "Usage: %s packagename [filename]"
      print "Download an app."
      print "If filename is not present, will write to packagename.apk."
      sys.exit(1)

  packagename = sys.argv[1]

  if (len(sys.argv) == 3):
      filename = sys.argv[2]
  else:
      filename = packagename + ".apk"
  download_sdk_to_file(packagename, filename)
  print "Done"

if __name__ == '__main__':
  main()
