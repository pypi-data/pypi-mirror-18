"""
sms command-line tool
"""

from configparser import ConfigParser
from pathlib import Path

from click import group, command, option, argument, echo, secho
import requests


config = ConfigParser()
if not config.read([str(Path('~/.nexmorc').expanduser())]):
    raise Exception("Missing config file!")

api_key = config.get('credentials', 'api_key')
api_secret = config.get('credentials', 'api_secret')


@command()
@option('-t', '--to')
@option('-f', '--from', '_from')
def main(to, _from):
    """ This tool doesn't work yet! """
    secho("This tool doesn't do anything yet!", fg='red')
