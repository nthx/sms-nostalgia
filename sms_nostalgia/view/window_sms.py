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


        align = gtk.Alignment()

        self.label_name = gtk.Label("")
        self.label_phone = gtk.Label("")
        self.label_when = gtk.Label("")
        self.label_message = gtk.Label("")
        self.label_message.set_line_wrap(True)
        self.photo = gtk.Image()
        self.photo.set_alignment(0, 0)
        self.photo.set_padding(0, 0)

        for label in [self.label_name, self.label_phone, self.label_when, self.label_message]:
            label.set_alignment(0, 0)

        vbox = gtk.VBox(False, 0)
        vbox.pack_start(self.label_name, False, False, 0)
        vbox.pack_start(self.label_phone, False, False, 0)
        vbox.pack_start(self.label_when, False, False, 0)
        vbox.pack_start(self.photo, False, False, 0)
        vbox.pack_start(self.label_message, False, True, 0)

        align.add(vbox)
        window.add(align)

        window.connect("destroy", self.controller.sms_details_closed)
        return window


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


    def _update_labels(self, sms):
        has_icon = sms.contact and sms.contact.has_icon() or False
        if has_icon:
            self.photo.set_from_file(sms.contact.ico_path)
        else:
            self.photo.clear()

        self.label_name.set_label(sms.display_name())
        self.label_phone.set_label(sms.phone)
        self.label_when.set_label(sms.when)
        self.label_message.set_label(sms.message)
        if sms.display_name() == sms.phone:
            self.label_name.hide()
        else:
            self.label_name.show()

        self.window.set_title(sms.display_type())


    def show_sms(self):
        sms = self.controller.current_sms
        log.debug(sms.as_text())

        if self.window:
            self._update_labels(sms)

        else:
            self.window = self.build()
            self._update_labels(sms)

            self.window.show_all()







