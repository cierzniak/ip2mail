# <editor-fold desc="Imports">
import logging
import os
import subprocess


# </editor-fold>
# <editor-fold desc="Start logger service">
def start_logger(filename=''):
    log = logging.getLogger('main')
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)-5.5s | %(message)s', '%Y-%m-%d %H:%M:%S')
    if filename:
        handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), '../logs/' + filename + '.log'))
        handler.setFormatter(formatter)
        log.addHandler(handler)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        log.addHandler(handler)
    return log


logger = start_logger()


# </editor-fold>
# <editor-fold desc="Do subprocess">
def run_bash(command, outfile):
    logger.debug('Call ' + command)
    subprocess.call(command + ' > ' + outfile, shell=True)

# </editor-fold>
