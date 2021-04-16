import re

from pyrogram import filters

from app import *

def reply_rule(regex, reply_message, max_per_day=3):
    already_replied = set()

    def callback(app, message):
        user = message.from_user.id

        if user not in already_replied or user == super_user:

            if user != super_user:
                callback.today += 1
                if callback.today > callback.max_per_day:
                    return

            already_replied.add(user)
            message.reply_text(reply_message)

    callback.already_replied = already_replied
    callback.max_per_day = max_per_day
    callback.today = 0

    rules.append(callback)
    app.on_message(omuc_group & filters.regex(regex, re.IGNORECASE))(callback)

re_ping = '\
^alo+|\
^kim bo+r|\
^foo$'

reply_rule(re_ping, '**Pong!!**')

re_hello = '\
^salom(?:\s+hammaga)?$|\
^(?:as)?salomu?\s+ala[yi]kum$\
'
reply_rule(re_hello, '**Salom**')
