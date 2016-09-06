# <editor-fold desc="Imports">
import logging
import os
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../config'))
import settings


# </editor-fold>
# <editor-fold desc="Log and print message">
def msg(message, debug=False):
    if (not debug) or (debug and settings.DEBUG):
        logging.info(str(datetime.now().replace(microsecond=0)) + ' | ' + message)
    if settings.DEBUG:
        print(str(datetime.now().replace(microsecond=0)) + ' | ' + message)

# </editor-fold>
