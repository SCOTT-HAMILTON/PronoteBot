
import click
from PronoteBot.pronotebot import PronoteBot
from json import load
from os import environ
from os.path import isfile, isdir, expanduser

@click.command()
@click.option('-p', '--page', type=click.INT)
def cli(page):
    """Pronote bot to open pronote or to open the physics and chemistry book at a specified page"""
    if page != None:
        print("Opening page ", page)

    config_file = environ['HOME']+'/.config/pronotebot.conf'
    assert isfile(config_file)
    config = load(open(config_file, 'r'))
    if 'firefox_profile' in config.keys():
        path = expanduser(config['firefox_profile'])
        assert isdir(path)
        bot = PronoteBot(firefox_profile=path)
    else:
        bot = PronoteBot()
    bot.start(page, config['username'], config['password'])
