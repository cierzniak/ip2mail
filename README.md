# Python IPv4 Email sender for Linux systems

Application to unattended connections of Linux servers to network eg. Raspberry Pi. Simple usage allow to use it everywhere.

### Dependencies
* Python 3

### Configuration
Copy file `config/settings.ini.py` to `config/settings.py` and edit to fit your settings:
````python
# Email recipient
EMAIL_TO = 'user@example.com'

# Subject topic eg. Machine name
SUBJECT_TOPIC = 'Raspberry Pi'

# SMTP server
SMTP_SERV = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'user@gmail.com'
SMTP_PSWD = 'super_secret_password'
````

### Chmod
Allow to execute files:
````bash
sudo chmod +x ./cron.sh
sudo chmod +x ./apps/Main.py
````

### Crontab
````bash
@reboot nohup /root/EmailIP/cron.sh &
````