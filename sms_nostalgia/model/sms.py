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
        self.when = when
        self.contact = None #Will be setup later if contact found in eBook


    def display_name(self):
        return self.name and self.name or self.phone


    def display_type(self):
        return self.TYPES.get(self.type)


    def sent(self):
        return self.type == self.TYPE_SENT


    def received(self):
        return self.type == self.TYPE_INBOX


    def matches(self, text):
        text = text and text.lower() or ''
        return text in (self.phone and self.phone or '')\
            or text in (self.message and self.message.lower() or '') \
            or text in (self.name and self.name.lower() or '') \
            or text in (self.when and self.when or '')


    def as_text(self):
        return '%s: %s; %s' % (self.display_type(), self.display_name(), self.message)
    
    __str__ = as_text
    __repr__ = as_text
