import logging
log = logging.getLogger(__name__)



class Sms(object):

    TYPE_INBOX = 0
    TYPE_SENT = 1

    def __init__(self, phone, message, type, when, name=None):

        self.phone = phone
        self.message = message
        self.type = type
        self.name = name

    def as_text(self):
        if self.name:
            return '%s: %s; %s' % (self.type, self.name, self.message)
        else:
            return '%s: %s; %s' % (self.type, self.phone, self.message)
    
    __str__ = as_text
    __repr__ = as_text
