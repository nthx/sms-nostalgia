import logging
log = logging.getLogger(__name__)

from sms_nostalgia.lib.contacts import ContactsAPI



class Contact(object):

    def __init__(self, econtact):
        self.econtact = econtact


    def uuid(self):
        return self.econtact.get_uid()


    def name(self):
        return self.econtact.get_name()


    def phones(self):
        phones = set()
        for phone_attr in ContactsAPI.phone_attributes:
            phone = self.econtact.get_property(phone_attr)
            if phone: phones.add(phone)

        return phones

