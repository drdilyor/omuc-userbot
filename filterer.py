import os

from pyrogram import Client
from pyrogram.types import Message

import colorlist
from app import app, omuc_group, mod_group
from ranker import get_score

ALLOW_MODS = os.environ.get('ALLOW_MODS', '')


async def on_sus(_app: Client, message: Message, score: int):
    # default, logs to console
    print('WARN sertifikatboz:', message.link, 'score:', score)


# noinspection PyShadowingNames
@app.on_message(omuc_group)
async def on_message(app: Client, message: Message):
    if not ALLOW_MODS and await app.get_chat_member(mod_group, message.from_user.id):
        return
    if message.text is None:
        return
    if await colorlist.on_message(app, message):
        return
    score = get_score(message.text)
    if score >= 7:
        await on_sus(app, message, score)
    else:
        print('no sus', message.link, score)
