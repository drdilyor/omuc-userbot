import os

from pyrogram import Client, filters

session = os.environ.get('SESSION', 'drdilyor')
if os.environ.get('MODE') == 'heroku':
    app = Client(session, os.environ['API_ID'], os.environ['API_HASH'])
else:
    # take api id and hash from config.ini
    app = Client(session)


omuc_group = (
    filters.chat('uzbekcoderslive')
    | filters.chat('fullstack_omuc')
    | filters.chat('frontend_omuc')
    | filters.chat(-512797745)  # test group
)
super_user = 1044136353
