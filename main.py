import logging
import asyncio
import signal

from app import app
import colorlist  # noqa
import db  # noqa
import filterer  # noqa
import reporter  # noqa

logging.basicConfig(level=logging.INFO)

asyncio.get_event_loop().run_until_complete(db.init())
asyncio.get_event_loop().run_until_complete(colorlist.init())

on_exit = lambda _, __: asyncio.get_event_loop().create_task(db.close())  # noqa
signal.signal(signal.SIGINT, on_exit)
signal.signal(signal.SIGTERM, on_exit)

app.run()
