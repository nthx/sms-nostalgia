import logging, sys
log = logging.getLogger(__name__)


root = None

def setup(r):
    global root
    root = r


def on_history_append():
    pass


def sms_clicked(treeview, path, view_column):
    index = path[0]
    log.debug(root.all_smses_dict[index].as_text())

