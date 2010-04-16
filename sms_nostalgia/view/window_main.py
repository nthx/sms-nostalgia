import logging
log = logging.getLogger(__name__)

import gobject
import gtk
import hildon
import sys


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

        window.add_toolbar(self.create_autocomplete_toolbar())
        window.set_title('Sms Nostalgia')
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
        self.text_entry.grab_focus()

        self.text_entry.connect("key-release-event", self.controller.on_toolbar_search, None)
        return toolbar


    def create_sms_list(self):
        self.tree_view = hildon.GtkTreeView(gtk.HILDON_UI_MODE_NORMAL)
        self.tree_view.connect("row-activated", self.controller.sms_clicked)

        def get_type_ico(column, cell, model, iter):
            sms = model.get_value(iter, 0)
            cell.set_property('pixbuf', sms.get_type_ico())
            cell.set_property('width', 52)

        def get_face_ico(column, cell, model, iter):
            sms = model.get_value(iter, 0)
            pixbuf = sms.contact and sms.contact.get_face_pixbuf_small()
            cell.set_property('pixbuf', pixbuf)
            cell.set_property('width', 52)

        def get_sms(column, cell, model, iter):
            sms = model.get_value(iter, 0)
            cell.set_property('markup', sms.as_html())
            cell.set_property('wrap-mode', gtk.WRAP_WORD_CHAR)


        state_rend = gtk.CellRendererPixbuf()
        state_col = gtk.TreeViewColumn("type", state_rend)
        state_col.set_cell_data_func(state_rend, get_type_ico)
        state_rend.set_property('width', 52)

        sms_rend = gtk.CellRendererText()
        face_rend = gtk.CellRendererPixbuf()

        sms_col = gtk.TreeViewColumn("sms", markup=0)

        sms_col.pack_start(face_rend)
        sms_col.pack_end(sms_rend, expand=True)

        sms_col.set_cell_data_func(face_rend, get_face_ico)
        sms_col.set_cell_data_func(sms_rend, get_sms)

        self.tree_view.append_column(state_col)
        self.tree_view.append_column(sms_col)


        self.reload()

        return self.tree_view


    def get_model(self):
        store = gtk.ListStore(object)
        for index, sms in enumerate(self.root.current_smses):
            store.insert(index, [sms])
        return store


    def reload(self):
        self.tree_view.set_model(self.get_model())

