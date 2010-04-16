import logging, sys
log = logging.getLogger(__name__)


from sms_nostalgia.model.contact import Contact

import gtk
import hildon


class WindowSms(object):

    def __init__(self, view, controller):
        self.view = view
        self.controller = controller

        self.window = None #created/destroyed when needed

    
    def build(self):
        log.debug('building sms window..')
        window = hildon.StackableWindow()
        toolbar = self.create_toolbar()
        window.add_toolbar(toolbar)

        self.label_message = gtk.Label("")
        self.label_message.set_line_wrap(True)
        self.label_message.set_property('wrap-mode', gtk.WRAP_WORD_CHAR)

        self.photo = gtk.Image()

        for label in [self.label_message, self.photo]:
            label.set_alignment(0, 0)
            label.set_padding(0, 0)

        self.other_smses = gtk.VBox(False, 0)

        vbox = gtk.VBox(False, 0)
        vbox.pack_start(self.photo, False, False, 0)
        vbox.pack_start(self.label_message, False, True, 0)
        vbox.pack_start(self.other_smses, False, True, 0)

        self.sms_box = vbox

        pannable_area = hildon.PannableArea()
        pannable_area.add_with_viewport(vbox)
        window.add(pannable_area)

        window.connect("destroy", self.controller.sms_details_closed)
        return window


    def _update_labels(self, sms):
        self.window.set_title(sms.display_type())

        if sms.contact:
            self.photo.set_from_pixbuf(sms.contact.get_face_pixbuf_big())
        else:
            self.photo.set_from_pixbuf(Contact.FACE_DEFAULT)
            #self.photo.clear()

        self.label_message.set_markup(sms.as_html_v2())

        self.sms_box.remove(self.other_smses)
        self.other_smses = gtk.VBox(False, 0)

        #self.other_smses.pack_start(gtk.Label('...'))
        log.debug('smses: %s' % len(sms.other_smses()))
        for other_sms in sorted(sms.other_smses(), key=lambda sms: sms.when, reverse=True):
            other_sms_box = gtk.HBox()
            sender_photo = gtk.Image()
            if other_sms.received():
                sender_photo.set_from_pixbuf(other_sms.contact.get_face_pixbuf_small())
            elif other_sms.sent():
                sender_photo.set_from_pixbuf(other_sms.get_type_ico())
            else:
                raise unknown()

            sms_label = gtk.Label()
            sms_label.set_markup(other_sms.as_html_as_other())
            sms_label.set_line_wrap(True)
            sms_label.set_property('wrap-mode', gtk.WRAP_WORD_CHAR)

            for x in [sms_label, sender_photo]:
                x.set_alignment(0, 0)
                x.set_padding(0, 0)

            other_sms_box.pack_start(sender_photo, False, True, 0)
            other_sms_box.pack_start(sms_label, False, True, 0)
            self.other_smses.pack_start(other_sms_box)
        self.sms_box.pack_start(self.other_smses, False, True, 0)


    def create_toolbar(self):
        toolbar = gtk.Toolbar()
        self.toolbar_prev = gtk.ToolButton(
            gtk.image_new_from_stock(gtk.STOCK_GO_BACK,
            gtk.ICON_SIZE_LARGE_TOOLBAR),
            "Back")
        toolbar.insert(self.toolbar_prev, 0)

        self.toolbar_next = gtk.ToolButton(
            gtk.image_new_from_stock(gtk.STOCK_GO_FORWARD,
            gtk.ICON_SIZE_LARGE_TOOLBAR),
            "Forward")
        toolbar.insert(self.toolbar_next, 1)

        self.toolbar_prev.connect("clicked", lambda x: self.controller.load_prev_sms())
        self.toolbar_next.connect("clicked", lambda x: self.controller.load_next_sms())
        return toolbar


    def show_sms(self):
        sms = self.controller.current_sms
        log.debug(sms.as_text())

        if not self.window:
            self.window = self.build()
        self._update_labels(sms)
        self.window.show_all()

