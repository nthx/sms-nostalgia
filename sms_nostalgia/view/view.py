import logging, sys
log = logging.getLogger(__name__)

import gtk
import hildon
import sys
import gobject

from sms_nostalgia.util import sms
from sms_nostalgia.model.sms import Sms
from sms_nostalgia.controller.controller import on_history_append, sms_clicked



root = None



def fill_in_window1(window):
    list = create_list()

    # pack the table into the scrolled window 
    pannable_area = hildon.PannableArea()
    pannable_area.add(list)
    window.add(pannable_area)


def create_list_store():
    # Create and populate history list model
    findSelect = gtk.ListStore(gobject.TYPE_STRING)

    iter = findSelect.append()
    findSelect.set(iter, 0, "Foo")

    iter = findSelect.append()
    findSelect.set(iter, 0, "Bar")

    iter = findSelect.append()
    findSelect.set(iter, 0, "Baz")
    return findSelect


def create_list():
    tree_view = hildon.GtkTreeView(gtk.HILDON_UI_MODE_NORMAL)
    tree_view.connect("row-activated", sms_clicked)
    renderer = gtk.CellRendererText()
    col = gtk.TreeViewColumn("Title", renderer, text=0)

    tree_view.append_column(col)

    # Set multiple selection mode
    #selection = tree_view.get_selection()
    #selection.set_mode(gtk.SELECTION_MULTIPLE)

    tree_view.set_model(get_model())

    return tree_view


def get_model():
    store = gtk.ListStore(gobject.TYPE_STRING)

    index = 0
    for sms in root.all_smses:
        str = sms.as_text()
        store.insert(index, [str])
        root.all_smses_dict[index] = sms
        index += 1

    return store


def create_common_toolbar():
    # Create find toolbar
    elem = create_list_store()
    toolbar = hildon.FindToolbar("Find", elem, 0)

    # Set item on index 0 as the current active
    toolbar.set_active(0)

    # Attach a callback to handle "history-append" signal
    toolbar.connect_after("history-append", on_history_append, None)
    return toolbar

    
def create_common_menu():
    pass

def app_quit(widget, data=None):
    gtk.main_quit()


def build_windows(r):
    log.debug('building windows..')
    global root
    root = r


    program = hildon.Program.get_instance()

    window1 = hildon.StackableWindow()
    window1.connect("destroy", app_quit)


    fill_in_window1(window1)

    common_toolbar = create_common_toolbar()
    #window_specific_toolbar = create_window_specific_toolbar()
    #program.set_common_toolbar(common_toolbar)
    window1.add_toolbar(common_toolbar)


    #menu = create_common_menu()
    #program.set_common_app_menu(menu)


    program.add_window(window1)
    window1.show_all()


    program.set_can_hibernate(True)
    gtk.main()


