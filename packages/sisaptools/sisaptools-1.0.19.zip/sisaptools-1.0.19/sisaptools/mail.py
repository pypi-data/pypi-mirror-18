# -*- coding: utf8 -*-

"""
Utilitats per enviar mails.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
from email.header import Header
from email.mime.text import MIMEText
import socket

from .constants import APP_CHARSET
from .aes import AESCipher


class Mail(object):
    """Classe principal a instanciar."""

    def __init__(self):
        """Inicialització de paràmetres."""
        self.srv = 'smtp.gmail.com'
        self.prt = 465
        self.usr = 'sisap@sisap.cat'
        self.pwd = 'USpkEc14ipbpi3bWEkn7sU2549cdiNpi \
                    YZbyO2roVuwtwgz0GKXg5amtS4nVTT75'
        self.me = 'SISAP <sisap@sisap.cat>'
        self.to = []
        self.cc = []
        self.subject = ''
        self.text = ''
        self.attachments = []

    def __construct(self):
        """Construcció del missatge, cridat per send."""
        self.message = MIMEMultipart()
        self.message['From'] = self.me
        self.message['To'] = COMMASPACE.join(self.to)
        self.message['Cc'] = COMMASPACE.join(self.cc)
        self.message['Date'] = formatdate(localtime=True)
        self.message['Subject'] = Header(self.subject, APP_CHARSET)
        self.message.attach(MIMEText(self.text, 'plain', APP_CHARSET))
        for filename, iterable in self.attachments:
            data = '\r\n'.join([', '.join(map(str, row)) for row in iterable])
            attachment = MIMEText(data, 'plain', APP_CHARSET)
            attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename=filename
            )
            self.message.attach(attachment)
        self.to += self.cc

    def __connect(self):
        """Connexió al servidor, cridat per send."""
        self.server = smtplib.SMTP_SSL(self.srv, self.prt)
        self.server.login(self.usr, AESCipher().decrypt(self.pwd))

    def send(self):
        """Enviament del mail."""
        if self.to or self.cc:
            self.__construct()
            self.__connect()
            self.server.sendmail(self.me, self.to, self.message.as_string())
            self.server.close()
