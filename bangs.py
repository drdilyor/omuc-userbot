import re

from pyrogram import filters
from zalgo import zalgo as Z̵̠̓a̸͉̅l̶̺̎g̵̞͝o̵͚̿

from app import app

commands = {}

def command(name):
    def decorator(f):
        commands[name] = f
        return f
    return decorator

@command('g')
def google(term):
    if term:
        return 'https://google.com/search?q=' + term.replace(' ', '+')

@command('z')
@command('zalgo')
def zalgo_command(text, zalgo=Z̵̠̓a̸͉̅l̶̺̎g̵̞͝o̵͚̿(
    numAccentsUp=(3, 8),
    numAccentsDown=(3, 8),
    numAccentsMiddle=(0, 1),
    maxAccentsPerLetter=8)
):
    if text:
        return zalgo.zalgofy(text)

@command('z0')
def zalgo_zero(text, zalgo=Z̵̠̓a̸͉̅l̶̺̎g̵̞͝o̵͚̿(maxAccentsPerLetter=2)):
    if text:
        return zalgo.zalgofy(text)


@command('hc')
@command('hecomes')
def zalgo_hecomes(text, hecomes=Z̵̠̓a̸͉̅l̶̺̎g̵̞͝o̵͚̿(
    numAccentsUp=(8, 10),
    numAccentsDown=(8, 10),
    numAccentsMiddle=(10, 15),
    maxAccentsPerLetter=99)
):
    if text:
        return hecomes.zalgofy(text)


@app.on_message(filters.me & filters.text & filters.regex('^!(\w+)(?:\s+(.*))?$', re.DOTALL))
def on_command(app, message):
    m = message.matches[0]
    user_command, arg = m.group(1), m.group(2)
    try:
        f = commands[user_command]
    except KeyError:
        return
    result = f(arg)
    if result:
        message.edit_text(result)

