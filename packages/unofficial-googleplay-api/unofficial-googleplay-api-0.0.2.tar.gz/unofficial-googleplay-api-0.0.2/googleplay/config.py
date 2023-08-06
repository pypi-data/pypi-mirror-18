import json
import os.path

LANG            = None
ANDROID_ID      = None
GOOGLE_LOGIN    = None
GOOGLE_PASSWORD = None
AUTH_TOKEN      = None

# separator used by search.py, categories.py, ...
SEPARATOR = ";"

def raw_input_with_default(name, default):
  print "{}[{}]: ".format(name, default)
  value = raw_input()
  return value.strip() if value.strip() != '' else default

_home = os.path.expanduser('~')

if __name__ == '__main__':

  if not os.path.isdir(os.path.join(_home, '.gplay/')):
    os.mkdir(os.path.join(_home, '.gplay/'))

  if not os.path.isfile(os.path.join(_home, '.gplay/config')):
    with open(os.path.join(_home, '.gplay/config'), 'wb') as f:
      LANG            = raw_input_with_default('LANG', 'en_US')
      ANDROID_ID      = raw_input_with_default('ANDROID_ID', 'xxxxxxxxxxxxxxxx')
      GOOGLE_LOGIN    = raw_input_with_default('GOOGLE_LOGIN', 'account@gmail.com')
      GOOGLE_PASSWORD = raw_input_with_default('GOOGLE_PASSWORD', '***')
      f.write(json.dumps(
        {
          'LANG':LANG,
          'ANDROID_ID':ANDROID_ID,
          'GOOGLE_LOGIN':GOOGLE_LOGIN,
          'GOOGLE_PASSWORD':GOOGLE_PASSWORD
        }
        ))
else:
  if os.path.isfile(os.path.join(_home, '.gplay/config')):
    with open(os.path.join(_home, '.gplay/config'), 'rb') as f:
      config = json.load(f)

      LANG            = config['LANG']
      ANDROID_ID      = config['ANDROID_ID']
      GOOGLE_LOGIN    = config['GOOGLE_LOGIN']
      GOOGLE_PASSWORD = config['GOOGLE_PASSWORD']
      AUTH_TOKEN      = None

  if any([each == None for each in [ANDROID_ID, GOOGLE_LOGIN, GOOGLE_PASSWORD]]):
      raise Exception("config not set run python -m googleplay.config")

