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

zalgo = Z̵̠̓a̸͉̅l̶̺̎g̵̞͝o̵͚̿()
zalgo.numAccentsUp = (3, 8)
zalgo.numAccentsDown = (1, 3)
zalgo.numAccentsMiddle = (0, 0)
zalgo.maxAccentsPerLetter = 6

@command('z')
@command('zalgo')
def zalgo_command(text):
    if text:
        # some zalgos are changing the width of the character on telegram
        # and spaces are getting less visible
        return zalgo.zalgofy(text)

hecomes = Z̵̠̓a̸͉̅l̶̺̎g̵̞͝o̵͚̿()
zalgo.numAccentsUp = (5, 15)
zalgo.numAccentsDown = (3, 10)
zalgo.numAccentsMiddle = (2, 7)
zalgo.maxAccentsPerLetter = 20

@command('hc')
@command('hecomes')
def zalgo_hecomes(text):
    if text:
        return hecomes.zalgofy(text)

@app.on_message(filters.me & filters.text & filters.regex('^!(\w+)(?:\s+(.*))?$'))
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

