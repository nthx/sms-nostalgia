import logging
log = logging.getLogger(__name__)

import os


from sms_nostalgia.model.sms import Sms
from sms_nostalgia.util.sms import import_smses


class Root(object):
    """Just contains all objects (data) used by the app
    """

    def __init__(self):
        self.all_smses = []
        self.all_smses_dict = {} #key=index in GtkList, value=Sms


    def build_data(self):
        log.debug('building data..')


        self.all_smses = import_smses()

