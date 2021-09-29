from pyrogram import Client
from pyrogram.types import Message

import filterer
from app import mod_group


async def on_sus(app: Client, message: Message, score: int):
    text = [
        f'*Sertifikat boz* #report',
        f'Go to message: {message.link}',
        f'Score: {score}',
        f'Message:\n__{message.text}__',
    ]
    sent_message = await app.send_message(mod_group, '\n'.join(text))
    message_count: 'int | str' = 0
    async for _ in app.search_messages(
            message.chat.id,
            from_user=message.from_user.id):
        message_count += 1
        if message_count > 200:
            # for performance reasons
            message_count = '>200'
            break
    text.insert(2, f'User message count: {message_count}')
    await sent_message.edit_text('\n'.join(text))


filterer.on_sus = on_sus
