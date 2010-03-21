#!/usr/bin/python
import logging, sys
log = logging.getLogger(__name__)

log_format = "%(message)s"
log_datefmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format, datefmt=log_format)


from sms_nostalgia import app

