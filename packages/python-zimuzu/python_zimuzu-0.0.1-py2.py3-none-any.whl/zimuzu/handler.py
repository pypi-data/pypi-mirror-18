# -*- coding:utf-8 -*-
from pprint import pprint, pformat

from .core import Handler


class PPrintHandler(Handler):
    def __init__(self, *pprint_args, **pprint_kwargs):
        super(PPrintHandler, self).__init__()
        self.pprint_args = pprint_args
        self.pprint_kwargs = pprint_kwargs

    def emit(self, record):
        pprint(record, *self.pprint_args, **self.pprint_kwargs)


class SMTPHandler(Handler):
    def __init__(self, mailhost, fromaddr, toaddrs, subject, credentials=None, secure=None, timeout=5.0):
        super(SMTPHandler, self).__init__()
        if isinstance(mailhost, (list, tuple)):
            self.mailhost, self.mailport = mailhost
        else:
            self.mailhost, self.mailport = mailhost, None
        if isinstance(credentials, (list, tuple)):
            self.username, self.password = credentials
        else:
            self.username = None
        self.fromaddr = fromaddr
        if isinstance(toaddrs, str):
            toaddrs = [toaddrs]
        self.toaddrs = toaddrs
        self.subject = subject
        self.secure = secure
        self.timeout = timeout

    def getSubject(self, record):
        """
        Determine the subject for the email.

        If you want to specify a subject line which is record-dependent,
        override this method.
        """
        return self.subject

    def emit(self, record):
        import smtplib
        from email.message import EmailMessage
        import email.utils

        port = self.mailport
        if not port:
            port = smtplib.SMTP_PORT
        smtp = smtplib.SMTP(self.mailhost, port, timeout=self.timeout)
        msg = EmailMessage()
        msg['From'] = self.fromaddr
        msg['To'] = ','.join(self.toaddrs)
        msg['Subject'] = self.getSubject(record)
        msg['Date'] = email.utils.localtime()
        msg.set_content(pformat(record))
        if self.username:
            if self.secure is not None:
                smtp.ehlo()
                smtp.starttls(*self.secure)
                smtp.ehlo()
            smtp.login(self.username, self.password)
        smtp.send_message(msg)
        smtp.quit()
