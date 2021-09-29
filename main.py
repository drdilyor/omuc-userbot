import logging

from app import app
import filterer  # noqa
import reporter  # noqa

logging.basicConfig(level=logging.INFO)

app.run()
