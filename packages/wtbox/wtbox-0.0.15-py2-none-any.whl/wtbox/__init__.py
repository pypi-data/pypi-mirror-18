

# IMPORTS WHICH SHOULD APPEAR IN emzed.ext AFTER INSTALLING THE PACKAGE:
from minimal_module import hello # makes emzed.ext.wtbox.hello() visible
from doc import read as documentation
# DO NOT TOUCH THE FOLLOWING LINE:
import pkg_resources
__version__ = tuple(map(int, pkg_resources.require(__name__)[0].version.split(".")))
del pkg_resources