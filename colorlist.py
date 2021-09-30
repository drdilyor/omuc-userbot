"""I called it so because I couldn't decide between 'blacklist' and 'whitelist'"""
import re

from Levenshtein import distance  # noqa
from pyrogram import Client, filters
from pyrogram.types import Message

from app import app as app_, mod_group
from db import Colorlist
from util import normalize_uzbek

colorlist: list['Colorlist']


async def init():
    global colorlist
    colorlist = await Colorlist.all()
    print(colorlist)


async def on_message(app: Client, message: Message):
    text = ''.join(re.findall('[ a-z0-9]', normalize_uzbek(message.text)))
    for i in colorlist:
        if distance(i.text, text) <= 2:
            if i.is_black:
                if await try_blocking(app, message):
                    await message.reply_text('Blacklisted message occured one more time.')
            return True
    return False


async def check_permissions(message: Message) -> bool:
    member = await message.chat.get_member(message.from_user.id)
    if member.can_restrict_members and member.can_delete_messages:
        return True
    else:
        await message.reply("You don't have enough permissions.\n"
                            "Permissions required: can_restrict_members, "
                            "can_delete_messages.")
        return True


async def try_blocking(app: Client, message: Message):
    if not check_permissions(message):
        return False
    try:
        await app.kick_chat_member(message.chat.id, message.from_user.id)
        await message.delete()
        await app.send_message(message.chat.id, 'Successfully blocked.')
    except Exception:  # noqa
        await notify_no_perms(app, message)
        return False
    else:
        return True


async def notify_no_perms(app: Client, message: Message):
    text = '*Blacklist*\nChat admin with restrict permission required in: ' \
           f'@{message.chat.username}.'
    await app.send_message(mod_group, text)


@app_.on_message(filters.regex('^!black$'))
async def on_black(app: Client, message: Message):
    if await add_to_list(message, True):
        await try_blocking(app, message.reply_to_message)


@app_.on_message(filters.regex('^!white$'))
async def on_white(_app: Client, message: Message):
    if not check_permissions(message):
        return
    await add_to_list(message, False)


async def add_to_list(message: Message, is_black: bool):
    if message.reply_to_message is None or message.reply_to_message.text is None:
        await message.reply_text('Must reply to a text message!')
        return False
    text = message.reply_to_message.text
    if text in ('!black', '!white'):
        await message.reply_text('Cannot blacklist a command!')
        return False
    new = Colorlist(text=text, is_black=is_black)
    await new.save()
    colorlist.append(new)
    await message.reply('Added successfully.')
    return True
