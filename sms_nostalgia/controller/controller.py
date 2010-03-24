import logging, sys
log = logging.getLogger(__name__)


import gtk
import hildon


class Controller(object):


    def __init__(self, root):
        self.root = root
        self.view = None #view setup later


    def app_quit(self, widget, data=None):
        gtk.main_quit()


    def sms_details_closed(self, widget):
        log.debug('sms_details_closed')

        self.view.window_sms.window.hide_all()
        self.view.window_sms.window = None
        #self.view.window_sms.label_name = None
        #self.view.window_sms.label_phone = None
        #self.view.window_sms.label_message = None
        #self.view.window_sms.toolbar_prev = None
        #self.view.window_sms.toolbar_next = None


    def on_history_append(self):
        pass


    def sms_clicked(self, treeview, path, view_column):
        index = path[0]
        sms = self.root.all_smses_dict[index]

        self.view.window_sms.show_sms(index, sms)


    def load_prev_sms(self, index, sms):
        if index > 0:
            prev_sms = self.root.all_smses_dict[index-1]
            self.view.window_sms.show_sms(index-1, prev_sms)


    def load_next_sms(self, index, sms):
        if index < len(self.root.all_smses_dict) - 1:
            next_sms = self.root.all_smses_dict[index+1]
            self.view.window_sms.show_sms(index+1, next_sms)


