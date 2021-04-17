from pyrogram import filters

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

