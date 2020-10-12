from pronotebot import PronoteBot
from json import load
from os import environ
from os.path import isfile, isdir, expanduser

config_file = environ['HOME']+'/.config/pronotebot.conf'
assert isfile(config_file)
config = load(open(config_file, 'r'))
if 'firefox_profile' in config.keys():
    path = expanduser(config['firefox_profile'])
    assert isdir(path)
    bot = PronoteBot(firefox_profile=path)
else:
    bot = PronoteBot()
bot.start(None, config['username'], config['password'])
