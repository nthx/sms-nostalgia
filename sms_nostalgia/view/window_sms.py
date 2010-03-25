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
        window.set_title("Sms Details")

        self.toolbar = self.create_toolbar()
        window.add_toolbar(self.toolbar)


        align = gtk.Alignment()

        self.label_name = gtk.Label("")
        self.label_phone = gtk.Label("")
        self.label_message = gtk.Label("")
        self.label_message.set_line_wrap(True)

        vbox = gtk.VBox(False, 0)
        vbox.pack_start(self.label_name, False, False, 0)
        vbox.pack_start(self.label_phone, False, False, 0)
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
        self.label_name.set_label(sms.display_name())
        self.label_phone.set_label(sms.phone)
        self.label_message.set_label(sms.message)


    def show_sms(self):
        sms = self.controller.current_sms
        log.debug(sms.as_text())

        if self.window:
            log.debug('exists.. updating labels')
            self._update_labels(sms)

        else:
            log.debug('new.. creating labels')
            self.window = self.build()
            self._update_labels(sms)

            self.window.show_all()







