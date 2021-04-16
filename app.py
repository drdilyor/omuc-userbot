import re

from pyrogram import Client, filters

app = Client('drdilyor')

omuc_group = (
    filters.chat('uzbekcoderslive')
    |filters.chat('fullstack_omuc')
    |filters.chat('frontend_omuc')
    |filters.chat(-512797745) # test group
)
super_user = 1044136353
