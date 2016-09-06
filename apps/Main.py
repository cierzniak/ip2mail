#!/usr/bin/env python3
# <editor-fold desc="Imports">
import logging
import os
import re
import smtplib
import subprocess
import sys
from email.mime.text import MIMEText

sys.path.append(os.path.join(os.path.dirname(__file__), '../functions'))
import other

sys.path.append(os.path.join(os.path.dirname(__file__), '../config'))
import settings

# </editor-fold>
logging.basicConfig(filename="./logs/main.log", level=logging.DEBUG)
content = ''
# <editor-fold desc="Get hostname">
other.msg('Try to find hostname')
subprocess.call('hostname >' + settings.FILE_HOST, shell=True)
# </editor-fold>
# <editor-fold desc="Read hostname">
try:
    with open(settings.FILE_HOST, 'r') as file:
        content += 'Hostname: ' + file.readline() + '\n'
except FileNotFoundError:
    other.msg('FAILED to open file with hostname')
# </editor-fold>
# <editor-fold desc="Get IPs of all interfaces">
other.msg('Try to find all network interfaces')
subprocess.call('ip -4 addr > ' + settings.FILE_IPV4, shell=True)
# </editor-fold>
# <editor-fold desc="Read IPs at network interfaces">
try:
    with open(settings.FILE_IPV4, 'r') as file:
        temp_interface = ''
        temp_ipaddress = ''
        temp_line_match = -1
        for idx, line in enumerate(file.readlines()):
            # Find line with interface name
            grep_line = re.match('^\d+: (.*):', line, re.IGNORECASE | re.MULTILINE)
            if grep_line:
                temp_interface = grep_line.group(1)
                temp_line_match = idx
                # Get IP of found interface
            if idx == temp_line_match + 1:
                grep_line = re.match('^ +inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/', line,
                                     re.IGNORECASE | re.MULTILINE)
                temp_ipaddress = grep_line.group(1)
                # Add info of interface and IP to list
                other.msg('Found interface ' + temp_interface + ' with IPv4 ' + temp_ipaddress)
                content += 'Found interface ' + temp_interface + ' with IPv4 ' + temp_ipaddress + '\n'
except FileNotFoundError:
    other.msg('FAILED to open file with IPs')
# </editor-fold>
# <editor-fold desc="Connect to SMTP server">
other.msg('Login to SMTP server ' + settings.SMTP_SERV + ':' + str(settings.SMTP_PORT))
smtpserver = smtplib.SMTP(settings.SMTP_SERV, settings.SMTP_PORT)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login(settings.SMTP_USER, settings.SMTP_PSWD)
# </editor-fold>
# <editor-fold desc="Send Email with data">
other.msg('Send Email')
msg = MIMEText(content, 'plain')
msg['Subject'] = '[' + settings.SUBJECT_TOPIC + '] IP Addresses'
msg['From'] = settings.SMTP_USER
msg['To'] = settings.EMAIL_TO
smtpserver.sendmail(settings.SMTP_USER, [settings.EMAIL_TO], msg.as_string())
smtpserver.quit()
# </editor-fold>
other.msg('Done')
