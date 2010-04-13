#!/usr/bin/python
import logging, sys
log = logging.getLogger(__name__)

#hack to use n900 missing dateutil lib
#TODO: try to import. If not found use attached lib
import sys
sys.path.append('sms_nostalgia/lib/')

log_format = "%(asctime)s: %(name)s: %(message)s"
log_datefmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format, datefmt=log_datefmt)


from sms_nostalgia import app

