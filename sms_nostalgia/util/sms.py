import logging
log = logging.getLogger(__name__)

from sms_nostalgia.model.contact import Contact
from sms_nostalgia.model.sms import Sms

from sms_nostalgia.lib.contacts import ContactsAPI

import csv
import os



def parse(path):
    file = None
    if os.path.exists(path) and os.path.isfile(path):
        file = open(path)
    else:
        return []

    smses = []
    for line in csv.reader(file, delimiter=';', quotechar='"'):
        sms = sms_parser_by_type(line[0], line[1], line)
        if sms: smses.append(sms)

    log.debug('Imported %s' % (len(smses)))
    return smses


def sms_parser_by_type(msg_type, sms_type, line):
    if 'sms' != msg_type:
        #mms not supported
        return

    if sms_type == 'submit':
        class SentParser(object):
            def parse(self, line):
                return Sms(
                    phone=line[3],
                    message=line[7],
                    type=Sms.TYPE_SENT, 
                    when=line[5])
        return SentParser().parse(line)

    elif sms_type == 'deliver':
        class InboxParser(object):
            def parse(self, line):
                return Sms(
                    phone=line[2],
                    message=line[7],
                    type=Sms.TYPE_INBOX, 
                    when=line[5])
        return InboxParser().parse(line)

    else:
        log.debug('unknown sms type: %s' % sms_type)



def retrieve_names_from_addressbook(smses):
    contacts_by_phone = ContactsAPI.sort_by_phone()
    for sms in smses:
        if sms.phone in contacts_by_phone:
            sms.contact = contacts_by_phone[sms.phone]
            sms.name = sms.contact.name()
    return smses


def import_smses():
    """
    @returns all smses (Inbox + Sent)
    """

    log.debug('importing sms..')


    smses = []
    smses.extend(parse(os.path.join('data', 'inbox.csv')))
    smses.extend(parse(os.path.join('data', 'sent.csv')))

    smses = retrieve_names_from_addressbook(smses)

    return smses

