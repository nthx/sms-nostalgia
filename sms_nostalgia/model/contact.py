import logging
log = logging.getLogger(__name__)

from sms_nostalgia.lib.contacts import ContactsAPI
import sms_nostalgia.lib.vobject as vobject

import gtk


class Contact(object):
    FACE_DEFAULT = gtk.gdk.pixbuf_new_from_file_at_size('/usr/share/icons/hicolor/48x48/hildon/general_default_avatar.png', 48, 48)

    def __init__(self, econtact):
        self.econtact = econtact
        self.vcard = None
        self.has_face_ico = None
        self.face_ico_path = None
        self.face_pixbuf_small = None
        self.face_pixbuf_big = None
        self.smses = []


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


    def add_sms(self, sms):
        sms.contact = self
        self.smses.append(sms)


    def sort_smses(self):
        self.smses = sorted(self.smses, key=lambda sms: sms.when)


    def has_face_icon(self):
        if self.has_face_ico in (True, False):
            return self.has_face_ico

        for line in self.get_vcard().lines():
            if 'PHOTO' == line.name:
                self.has_face_ico = True
                self.face_ico_path = line.value.replace('file://', '')
                self.face_pixbuf_small = gtk.gdk.pixbuf_new_from_file_at_size(self.face_ico_path, 48, 48)
                return self.has_face_ico

        self.has_face_ico = False


    def get_face_pixbuf_small(self):
        if self.has_face_icon():
            return self.face_pixbuf_small
        return self.FACE_DEFAULT


    def get_face_pixbuf_big(self):
        if self.has_face_icon():
            if not self.face_pixbuf_big:
                self.face_pixbuf_big = gtk.gdk.pixbuf_new_from_file_at_size(self.face_ico_path, 192, 192)
            return self.face_pixbuf_big
        return None


