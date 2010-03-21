import logging
log = logging.getLogger(__name__)


from model.root import Root
from view import view
from controller import controller


root = Root()
root.build_data()

controller.setup(root)
view.build_windows(root)

