
import click
from PronoteBot.pronotebot import PronoteBot
from json import load
from os import environ
from os.path import isfile

@click.command()
@click.option('-p', '--page', type=click.INT)
def cli(page):
    """Pronote bot to open pronote or to open the physics and chemistry book at a specified page"""
    if page != None:
        print("Opening page ", page)

    config_file = environ['HOME']+'/.config/pronotebot.conf'
    assert isfile(config_file)
    config = load(open(config_file, 'r'))
    bot = PronoteBot()
    bot.start(page, config['username'], config['password'])
