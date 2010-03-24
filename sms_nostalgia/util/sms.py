import logging
log = logging.getLogger(__name__)

from sms_nostalgia.model.sms import Sms

import csv
import os



def parse(path, type):
    file = None
    if os.path.exists(path) and os.path.isfile(path):
        file = open(path)
    else:
        return []

    result = []
    for line in csv.reader(file, delimiter=';', quotechar='"'):
        if line[0] == 'sms' and line[1] == 'submit':
            sms = Sms(phone=line[3],
                      message=line[7],
                      type=type, 
                      when=line[5],
                      name=line[3])
            result.append(sms)
    log.debug('Imported %s of %s' % (len(result), type))
    return result


def import_smses():
    """
    @returns all smses (Inbox + Sent)
    """

    log.debug('importing sms..')


    result = []
    result.extend(parse(os.path.join('data', 'inbox.csv'), Sms.TYPE_INBOX))
    result.extend(parse(os.path.join('data', 'sent.csv'), Sms.TYPE_SENT))
    return result

