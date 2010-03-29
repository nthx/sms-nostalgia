import logging
log = logging.getLogger(__name__)

import gtk
import hildon


from sms_nostalgia.view.window_main import WindowMain
from sms_nostalgia.view.window_sms import WindowSms



class View(object):

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller


        self.label_sms_msg = None
        self.label_sms_phone = None
        self.label_sms_number = None


        self.window_main = WindowMain(root, self, controller)
        self.window_sms = WindowSms(self, controller)


        program = hildon.Program.get_instance()

        program.add_window(self.window_main.window)
        self.window_main.window.show_all()

        #program.set_common_toolbar(common_toolbar)
        #program.set_common_app_menu(common_menu)

        program.set_can_hibernate(True)



    def start(self):
        log.debug('started')
        self.window_main.text_entry.grab_focus()
        gtk.main()
        




        



