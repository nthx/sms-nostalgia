import logging, sys
log = logging.getLogger(__name__)


import gtk
import hildon


class Controller(object):

    def __init__(self, root):
        self.root = root
        self.view = None #view setup later

        self.current_sms = None


    def store_current_sms(self, sms):
        self.current_sms = sms


    def app_quit(self, widget, data=None):
        gtk.main_quit()


    def sms_details_closed(self, widget):
        log.debug('sms_details_closed')

        self.view.window_sms.window.hide_all()
        self.view.window_sms.window = None


    def on_history_append(self):
        pass


    def on_toolbar_search(self, entry, event, z):
        log.debug('on_toolbar_search')
        log.debug(entry.get_text())
        filtered = self.root.filter_smses(entry.get_text())
        if filtered:
            self.view.window_main.reload()
            if self.root.current_smses:
                self.current_sms = self.root.current_smses[0]
            else:
                self.current_sms = None


    def sms_clicked(self, treeview, path, view_column):
        index = path[0]
        self.store_current_sms(self.root.current_smses[index])
        self.view.window_sms.show_sms()


    def load_prev_sms(self):
        index = self.root.current_smses.index(self.current_sms)
        if index > 0 and len(self.root.current_smses):
            self.store_current_sms(self.root.current_smses[index-1])
            self.view.window_sms.show_sms()


    def load_next_sms(self):
        index = self.root.current_smses.index(self.current_sms)
        if index < len(self.root.current_smses) - 1:
            self.store_current_sms(self.root.current_smses[index+1])
            self.view.window_sms.show_sms()


