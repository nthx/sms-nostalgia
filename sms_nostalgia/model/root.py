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
        self.current_smses = []
        self.sms_by_index = {} #key=index in GtkList, value=Sms

    def filter_smses(self, text):
        if not text or len(text) <= 2:
            return
        self.current_smses = [sms for sms in self.all_smses if sms.matches(text)]
        return True


    def build_data(self):
        log.debug('building data..')

        self.all_smses = import_smses()

        log.debug('sorting..')
        self.all_smses = sorted(self.all_smses, key=lambda sms: sms.when, reverse=True)
        self.current_smses = self.all_smses[:]


