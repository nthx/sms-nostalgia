#!/usr/bin/python
import logging, sys
log = logging.getLogger(__name__)

log_format = "%(asctime)s: %(name)s: %(message)s"
log_datefmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format, datefmt=log_datefmt)


from sms_nostalgia import app

