#!/usr/bin/python
import logging
log = logging.getLogger(__name__)

import sys
from sms_nostalgia import app


log_format = "%(asctime)s %(levelname)-1.1s %(message)s"
log_datefmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format, datefmt=log_format)


if __name__ == "__main__":
    app.start()

