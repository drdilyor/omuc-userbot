import re
import time
import threading

from pyrogram import filters
import schedule

from app import *

rules = []

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

    def reset_daily_count():
        # I hope there will not occur race conditions
        # Because people usually don't chat at 0 am :P
        callback.today = 0

    callback.already_replied = already_replied
    callback.max_per_day = max_per_day
    callback.today = 0

    rules.append(callback)
    schedule.every().day.at('00:00').do(reset_daily_count) 
    app.on_message(omuc_group & filters.regex(regex, re.IGNORECASE))(callback)

re_ping = '\
^alo+|\
^kim bo+r(?:\s+.{,10})?$|\
^foo$'

reply_rule(re_ping, '**Pong!!**')

everyone = '(?:\s+(?:hammaga|barchaga))?'
re_hello = f'\
^salom{everyone}$|\
^(?:as)?salomu?\s+al[ae][yi]kum{everyone}$\
'
reply_rule(re_hello, '**Salom**')

def run_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_jobs, daemon=True).start()
