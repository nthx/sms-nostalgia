import logging
log = logging.getLogger(__name__)



class Sms(object):

    TYPE_INBOX = 0
    TYPE_SENT = 1

    TYPES = {}
    TYPES[TYPE_INBOX] = 'Inbox'
    TYPES[TYPE_SENT] = 'Sent'


    def __init__(self, phone, message, type, when, name=None):
        self.phone = phone
        self.message = message
        self.type = type
        self.name = name
        self.contact = None #Will be setup later if contact found in eBook


    def display_name(self):
        return self.name and self.name or self.phone


    def display_type(self):
        return self.TYPES.get(self.type)


    def as_text(self):
        return '%s: %s; %s' % (self.display_type(), self.display_name(), self.message)
    
    __str__ = as_text
    __repr__ = as_text
