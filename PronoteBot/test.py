from base64 import b64encode
from getpass import getpass
from json import load
from os import environ
from os.path import isfile, isdir, expanduser
from pronotebot import PronoteBot

config_file = environ['HOME']+'/.config/pronotebot.conf'
assert isfile(config_file)
config = load(open(config_file, 'r'))
password = getpass()
if 'firefox_profile' in config.keys():
    path = expanduser(config['firefox_profile'])
    assert isdir(path)
    bot = PronoteBot(firefox_profile=path)
else:
    bot = PronoteBot()
bot.start(config['username'], b64encode(password.encode("UTF-8")).decode("UTF-8"))
