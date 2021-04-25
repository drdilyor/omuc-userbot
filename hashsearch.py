import functools

from pyrogram import filters

from app import *

hash_search_chat = 'uzbekcoderslive'

def hash_search(search_messages, text):
    if not text:
        return
    hashtag = text.split()[0]

    if not hashtag.startswith('#'):
        hashtag = '#' + hashtag

    query = f'#userbottagged {hashtag}'
    print(f'{query=}')

    msg = list(search_messages(hash_search_chat, query, limit=1, from_user=super_user))
    if not msg:
        return
    else:
        msg = msg[0]
    
    m = msg.reply_to_message
    if m.text:
        return m.text.markdown
    else:
        return m.link

@app.on_message(
    filters.text
    & ( ( filters.regex('^(#\w+)$') & filters.me)
      | ( omuc_group
        & filters.regex('^(?:@\w+\s+)?(#\w+)$')
        & filters.mentioned)
    )
)
def hash_searcher(app, message):
    m = message.matches[0]
    res = hash_search(app.search_messages, m.group(1))
    print(f'{res=}')
    if res:
        if message.from_user.is_self:
            message.edit_text(res)
        else:
            reply = message.reply_to_message and message.reply_to_message.message_id
            app.send_message(
                chat_id=message.chat.id, text=res,
                reply_to_message_id=reply
            )
            try:
                app.delete_messages(message.chat.id, message.id)
            except :
                pass
