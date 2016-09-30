# Python IPv4 Email sender for Linux systems

Application to unattended connections of Linux servers to network and sending email with IPv4 settings. Simple usage allow to use it everywhere.

### Dependencies
* Bash
* Python

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

* `EMAIL_TO` is recipient email,
* `SUBJECT_TOPIC` is prefix of subject, eg. [Server] Backup,
* `SMTP_(...)` are settings of SMTP server like address, port, user and password.

### Execute rights
Allow to execute files:

````bash
sudo chmod +x ./*.sh
sudo chmod +x ./apps/*.py
````

### Schedule
On Linux powered machine add scheduler using `crontab -e` by adding at the end of file:

````bash
@reboot /root/EmailIP/startup.sh
````

which means to send email on every start of server.

# Author
[Paweł Cierzniakowski](mailto:pawel@cierzniakowski.pl)
