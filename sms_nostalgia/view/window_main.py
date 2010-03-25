import logging
log = logging.getLogger(__name__)


import gobject
import gtk
import hildon



class WindowMain(object):

    def __init__(self, root, view, controller):
        self.root = root
        self.view = view
        self.controller = controller

        self.window = self.build()


    def build(self):
        log.debug('building main..')

        window = hildon.StackableWindow()
        window.connect("destroy", self.controller.app_quit)


        self.fill_panable_area(window)

        window.add_toolbar(self.create_toolbar())
        return window


    def fill_panable_area(self, window):
        sms_list = self.create_sms_list()

        # pack the table into the scrolled window 
        pannable_area = hildon.PannableArea()
        pannable_area.add(sms_list)
        window.add(pannable_area)


    def create_toolbar(self):
        # Create find toolbar
        elem = self.toolbar_find_store()
        toolbar = hildon.FindToolbar("Find", elem, 0)

        # Set item on index 0 as the current active
        toolbar.set_active(0)

        # Attach a callback to handle "history-append" signal
        toolbar.connect_after("history-append", self.controller.on_history_append, None)
        return toolbar


    def toolbar_find_store(self):
        # Create and populate history list model
        findSelect = gtk.ListStore(gobject.TYPE_STRING)

        iter = findSelect.append()
        findSelect.set(iter, 0, "Foo")

        iter = findSelect.append()
        findSelect.set(iter, 0, "Bar")

        iter = findSelect.append()
        findSelect.set(iter, 0, "Baz")
        return findSelect


    def create_sms_list(self):
        tree_view = hildon.GtkTreeView(gtk.HILDON_UI_MODE_NORMAL)
        tree_view.connect("row-activated", self.controller.sms_clicked)
        renderer = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Title", renderer, text=0)

        tree_view.append_column(col)

        tree_view.set_model(self.get_model())

        return tree_view


    def get_model(self):
        store = gtk.ListStore(gobject.TYPE_STRING)

        index = 0
        for sms in self.root.all_smses:
            str = sms.as_text()
            store.insert(index, [str])
            self.root.all_smses_dict[index] = sms
            index += 1

        return store

