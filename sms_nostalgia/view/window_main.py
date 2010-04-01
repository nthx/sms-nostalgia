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

        self.text_entry = None
        self.tree_view = None

        self.window = self.build()


    def build(self):
        log.debug('building main..')

        window = hildon.StackableWindow()
        window.connect("destroy", self.controller.app_quit)

        self.fill_panable_area(window)

        #window.add_toolbar(self.create_find_toolbar())
        window.add_toolbar(self.create_autocomplete_toolbar())
        return window


    def fill_panable_area(self, window):
        sms_list = self.create_sms_list()

        # pack the table into the scrolled window 
        pannable_area = hildon.PannableArea()
        pannable_area.add(sms_list)
        window.add(pannable_area)


    def create_autocomplete_toolbar(self):
        toolbar = gtk.Toolbar()

        label = gtk.Label("Find:")
        label.set_alignment(0, 0)

        self.text_entry = gtk.Entry()

        item1 = gtk.ToolItem()
        item1.add(label)
        item2 = gtk.ToolItem()
        item2.add(self.text_entry)

        toolbar.insert(item2, 0)
        toolbar.insert(item1, 0)

        self.text_entry.connect("key-release-event", self.controller.on_toolbar_search, None)
        return toolbar


    def create_find_toolbar(self):
        elem = self.toolbar_find_store()
        toolbar = hildon.FindToolbar("Find", elem, 0)
        toolbar.highlight_entry(get_focus=True)

        # Set item on index 0 as the current active
        toolbar.set_active(0)

        # Attach a callback to handle "history-append" signal
        toolbar.connect_after("history-append", self.controller.on_history_append, None)
        return toolbar


    def toolbar_find_store(self):
        # Create and populate history list model
        findSelect = gtk.ListStore(gobject.TYPE_STRING)

        #iter = findSelect.append()
        #findSelect.set(iter, 0, "Baz")

        return findSelect


    def create_sms_list(self):
        self.tree_view = hildon.GtkTreeView(gtk.HILDON_UI_MODE_NORMAL)
        self.tree_view.connect("row-activated", self.controller.sms_clicked)
        renderer = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Title", renderer, text=0)

        self.tree_view.append_column(col)

        self.reload()

        return self.tree_view


    def get_model(self):
        store = gtk.ListStore(gobject.TYPE_STRING)

        index = 0
        for sms in self.root.current_smses:
            str = sms.as_text()
            store.insert(index, [str])
            self.root.sms_by_index[index] = sms
            index += 1

        return store

    def reload(self):
        self.tree_view.set_model(self.get_model())

