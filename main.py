import asyncio
import logging
import os

import colorlist  # noqa
import db  # noqa
import filterer  # noqa
import reporter  # noqa
from app import app

logging.basicConfig(level=logging.INFO)

asyncio.get_event_loop().run_until_complete(db.init())
asyncio.get_event_loop().run_until_complete(colorlist.init())

app.run()
os.system(f'kill -9 {os.getpid()}')
