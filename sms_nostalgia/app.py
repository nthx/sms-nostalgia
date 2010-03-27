import logging
log = logging.getLogger(__name__)


from model.root import Root
from view.view import View
from controller.controller import Controller


root = Root()
root.build_data()

controller = Controller(root)
view = View(root, controller)

controller.view = view


view.start()
