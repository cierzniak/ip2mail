#!/usr/bin/env python
# <editor-fold desc="Imports">
import os
import re
import smtplib
import sys
from datetime import datetime
from email import encoders

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sys.path.append(os.path.join(os.path.dirname(__file__), '../functions'))
import other

sys.path.append(os.path.join(os.path.dirname(__file__), '../config'))
import settings

# </editor-fold>
logger = other.start_logger('main')
logger.info('>> Create new mail with IPv4 info')
text = 'Server runs at ' + str(datetime.now().replace(microsecond=0)) + '\n\n'
# <editor-fold desc="Get data">
logger.debug('Try to find hostname')
other.run_bash('hostname', settings.FILE_HOST)
logger.debug('Try to find all network interfaces')
other.run_bash('ip -4 addr', settings.FILE_IPV4)
logger.debug('Try to get dmesg log')
other.run_bash('dmesg', settings.FILE_DMESG)
# </editor-fold>
# <editor-fold desc="Read hostname">
try:
    with open(settings.FILE_HOST, 'r') as file:
        text += 'Hostname: ' + file.readline() + '\n'
except FileNotFoundError:
    logger.critical('FAILED to open file with hostname')
# </editor-fold>
# <editor-fold desc="Read IPs at network interfaces">
try:
    with open(settings.FILE_IPV4, 'r') as file:
        temp_interface = ''
        temp_ipaddress = ''
        temp_line_match = -1
        for idx, line in enumerate(file.readlines()):
            grep_line = re.match('^\d+: (.*):', line, re.IGNORECASE | re.MULTILINE)
            if grep_line:
                temp_interface = grep_line.group(1)
                temp_line_match = idx
            if idx == temp_line_match + 1:
                grep_line = re.match('^ +inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/', line,
                                     re.IGNORECASE | re.MULTILINE)
                temp_ipaddress = grep_line.group(1)
                logger.info('Found interface ' + temp_interface + ' with IPv4 ' + temp_ipaddress)
                text += 'Found interface ' + temp_interface + ' with IPv4 ' + temp_ipaddress + '\n'
except FileNotFoundError:
    logger.critical('FAILED to open file with IPs')
text += '\n'
# </editor-fold>
# <editor-fold desc="Connect to SMTP server">
logger.info('Login to SMTP server ' + settings.SMTP_SERV + ':' + str(settings.SMTP_PORT))
smtpserver = smtplib.SMTP(settings.SMTP_SERV, settings.SMTP_PORT)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login(settings.SMTP_USER, settings.SMTP_PSWD)
# </editor-fold>
# <editor-fold desc="Send Email with data">
logger.info('Sending email')
msg = MIMEMultipart()
msg['Subject'] = '[' + settings.SUBJECT_TOPIC + '] IP Addresses'
msg['From'] = settings.SMTP_USER
msg['To'] = settings.EMAIL_TO
logger.debug('Add attachments (dmesg.txt)')
with open(settings.FILE_DMESG, "rb") as file_:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(file_.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename=" + os.path.basename(settings.FILE_DMESG))
    msg.attach(part)
    text += 'Add attachment: '
    text += os.path.basename(settings.FILE_DMESG)
msg.attach(MIMEText(text, 'plain'))
smtpserver.sendmail(settings.SMTP_USER, [settings.EMAIL_TO], msg.as_string())
smtpserver.quit()
# </editor-fold>
logger.debug('> Done')
