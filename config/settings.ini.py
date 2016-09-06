import os

# Debug
DEBUG = False

# Email recipient
EMAIL_TO = 'user@example.com'

# Subject topic eg. Machine name
SUBJECT_TOPIC = 'Raspberry Pi'

# SMTP server
SMTP_SERV = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'user@gmail.com'
SMTP_PSWD = 'super_secret_password'

# <editor-fold desc="Do not touch unless you know what are you doing!">
FILE_IPV4 = os.path.join(os.path.dirname(__file__), '../data/ipv4.txt')
FILE_HOST = os.path.join(os.path.dirname(__file__), '../data/host.txt')
# </editor-fold>
