import logging
log = logging.getLogger(__name__)

import gtk
import hildon
import sys
import gobject

from util import sms
from model.sms import Sms


log_format = "%(asctime)s %(levelname)-1.1s %(message)s"
log_datefmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format, datefmt=log_format)


store = None
all_smses = []
all_smses_dict = {} #key=index in GtkList, value=Sms



def on_history_append():
    pass


def sms_clicked(treeview, path, view_column):
    index = path[0]
    log.debug('sms_clicked: %s' % index)
    log.debug(all_smses_dict[index].as_text())


def fill_in_window1(window):
    table = create_table()
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
    global all_smses, all_smses_dict
    store = gtk.ListStore(gobject.TYPE_STRING)

    log.debug(all_smses)

    index = 0
    for sms in all_smses:
        str = sms.as_text()
        store.insert(index, [str])
        all_smses_dict[index] = sms
        index += 1

    #store.connect("clicked", lambda: sms_clicked(i))

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

    
def create_table():
    # create a table of 10 by 10 squares. 
    table = gtk.Table (10, 10, False)

    # set the spacing to 10 on x and 10 on y 
    table.set_row_spacings(10)
    table.set_col_spacings(10)

    table.show()

    # this simply creates a grid of toggle buttons on the table
    # to demonstrate the scrolled window. 
    for i in range(10):
        for j in range(10):
            data_buffer = "button (%d,%d)\n" % (i, j)
            button = gtk.ToggleButton(data_buffer)
            table.attach(button, i, i+1, j, j+1)

    return table


def create_common_menu():
    pass

def app_quit(widget, data=None):
    gtk.main_quit()


def start():
    log.debug('start')
    global all_smses

    log.debug('building model')
    all_smses = sms.import_smses()


    program = hildon.Program.get_instance()

    window1 = hildon.StackableWindow()
    window1.connect("destroy", app_quit)


    fill_in_window1(window1)

    common_toolbar = create_common_toolbar()
    #window_specific_toolbar = create_window_specific_toolbar()
    #program.set_common_toolbar(common_toolbar)
    window1.add_toolbar(common_toolbar)



    #menu = create_common_menu()
    #program.set_common_app_menu (menu)



    program.add_window(window1)
    window1.show_all()


    program.set_can_hibernate (True)
    gtk.main()


