import logging, sys
log = logging.getLogger(__name__)


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
        self.toolbar = self.create_toolbar()
        window.add_toolbar(self.toolbar)

        self.label_message = gtk.Label("")
        self.label_message.set_line_wrap(True)
        self.label_message.set_property('wrap-mode', gtk.WRAP_WORD_CHAR)

        self.photo = gtk.Image()

        for label in [self.label_message, self.photo]:
            label.set_alignment(0, 0)
            label.set_padding(0, 0)

        vbox = gtk.VBox(False, 0)
        vbox.pack_start(self.photo, False, False, 0)
        vbox.pack_start(self.label_message, False, True, 0)

        pannable_area = hildon.PannableArea()
        pannable_area.add_with_viewport(vbox)
        window.add(pannable_area)

        window.connect("destroy", self.controller.sms_details_closed)
        return window


    def _update_labels(self, sms):
        has_face_icon = sms.contact and sms.contact.has_face_icon() or False
        if has_face_icon:
            self.photo.set_from_pixbuf(sms.contact.get_face_pixbuf_big())
        else:
            self.photo.clear()

        self.label_message.set_markup(sms.as_html_v2())
        self.window.set_title(sms.display_type())


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

        if self.window:
            self._update_labels(sms)

        else:
            self.window = self.build()
            self._update_labels(sms)

            self.window.show_all()







