import logging
log = logging.getLogger(__name__)

from sms_nostalgia.lib.contacts import ContactsAPI
import sms_nostalgia.lib.vobject as vobject



class Contact(object):

    def __init__(self, econtact):
        self.econtact = econtact
        self.vcard = None
        self.has_ico = None
        self.ico_path = None


    def uuid(self):
        return self.econtact.get_uid()


    def name(self):
        return self.econtact.get_name()


    def get_vcard(self):
        if not self.vcard:
            self.vcard = vobject.readOne(self.econtact.get_vcard_string())
        return self.vcard


    def phones(self):
        phones = set()

        for phone in self.phones_from_ctypes():
        #for phone in self.phones_from_vobject_slow():
            if phone: 
                yield phone


    def phones_from_vobject_slow(self):
        #vcard parsing implementation: SLOW
        for line in self.get_vcard().lines():
            if 'TEL' == line.name and line.value:
                yield line.value


    def phones_from_ctypes(self):
        #initial implementation... not returning all phones..
        for phone_attr in ContactsAPI.phone_attributes:
            phone = self.econtact.get_property(phone_attr)
            if phone: 
                yield phone


    def has_icon(self):
        log.debug('has_icon: %s' % self.name())
        if self.has_ico in (True, False):
            log.debug(self.has_ico)
            return self.has_ico
        log.debug('not yet know..')

        for line in self.get_vcard().lines():
            if 'PHOTO' == line.name:
                self.has_ico = True
                self.ico_path = line.value.replace('file://', '')
                log.debug(self.ico_path)
                log.debug(self.has_ico)
                return self.has_ico

        log.debug(False)
        self.has_ico = False


