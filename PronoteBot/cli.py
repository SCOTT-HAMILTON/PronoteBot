
import click
from PronoteBot.pronotebot import PronoteBot
from json import load
from os import environ
from os.path import isfile, isdir, expanduser
from enum import Enum

class Method(Enum):
    PAGE_NUMBER = 1
    DOWNLOAD = 2

class ChoiceMethod():
    def __init__(self, method, page_number=None):
        self.method = method
        if self.method == Method.PAGE_NUMBER:
            if page_number == None:
                print("Error, can't make page method without page number")
                return
            self.page_number = page_number

class ChoiceMethodParamType(click.ParamType):
    name = "page=<page_number>|download"

    def convert(self, value, param, ctx):
        print("converting...")
        tab = value.split("=")
        if value == 'download':
            return ChoiceMethod(Method.DOWNLOAD)
        elif tab[0] == 'page':
            try:
                return ChoiceMethod(Method.PAGE_NUMBER, int(tab[1]))
            except:
                self.fail(
                    "Expected a valid page number "
                    f"{value!r} of type {type(value).__name__}",
                    param,
                    ctx,
                )
        else:
            self.fail(
                "Expected either page or download method"
                f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )

@click.command()
@click.option('-m', '--method', type=ChoiceMethodParamType())
def cli(method):
    """Pronote bot to open pronote or to open the physics and chemistry book at a specified page"""
    config_file = environ['HOME']+'/.config/pronotebot.conf'
    config = load(open(config_file, 'r'))
    if 'firefox_profile' in config.keys():
        path = expanduser(config['firefox_profile'])
        assert isdir(path)
        bot = PronoteBot(firefox_profile=path)
    else:
        bot = PronoteBot()
    if method == None:
        bot.start(config['username'], config['password'])
    else:
        assert isfile(config_file)
        page_number = None
        download = False
        if method.method == Method.DOWNLOAD:
            download = True
        elif method.method == Method.PAGE_NUMBER:
            page_number = method.page_number
        bot.start(config['username'], config['password'], page_number=page_number, download=download)
