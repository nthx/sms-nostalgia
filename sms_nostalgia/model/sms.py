import logging
log = logging.getLogger(__name__)

import cgi
import datetime
import gtk


class Sms(object):

    TYPE_INBOX = 0
    TYPE_SENT = 1

    TYPES = {}
    TYPES[TYPE_INBOX] = 'Inbox'
    TYPES[TYPE_SENT] = 'Sent'

    TYPES_ICONS = {}
    TYPES_ICONS[TYPE_INBOX] = gtk.gdk.pixbuf_new_from_file_at_size('/usr/share/icons/hicolor/48x48/hildon/general_sms.png', 48, 48)
    TYPES_ICONS[TYPE_SENT] = gtk.gdk.pixbuf_new_from_file_at_size('/usr/share/icons/hicolor/48x48/hildon/chat_replied_sms.png', 48, 48)


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


    def get_type_ico(self):
        return self.TYPES_ICONS.get(self.type)


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
        return '%s: n%s' % (self.display_name(), self.message)

    
    def as_html(self):
        when = self.when
        try:
            when = datetime.datetime.strptime(self.when, '%Y.%m.%d %H:%M')
            when = when.strftime('%Y.%m.%d | %H:%M')
        except Exception, e:
            log.debug(e)
            pass
        return """\
<span weight="bold">%s</span> <span size="x-small" weight="light" foreground="#BBBBBB"><sup>%s</sup></span>
<span size="x-small" foreground="#BBBBBB">%s</span>""" \
            % (cgi.escape(self.display_name()), when, cgi.escape(self.message))

    
    __str__ = as_text
    __repr__ = as_text
