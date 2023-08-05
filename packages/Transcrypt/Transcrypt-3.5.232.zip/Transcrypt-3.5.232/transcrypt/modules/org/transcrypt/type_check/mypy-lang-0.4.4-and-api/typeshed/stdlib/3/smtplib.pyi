# Stubs for smtplib (Python 3.4)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class SMTPException(OSError): ...
class SMTPServerDisconnected(SMTPException): ...

class SMTPResponseException(SMTPException):
    smtp_code = ... # type: Any
    smtp_error = ... # type: Any
    args = ... # type: Any
    def __init__(self, code, msg) -> None: ...

class SMTPSenderRefused(SMTPResponseException):
    smtp_code = ... # type: Any
    smtp_error = ... # type: Any
    sender = ... # type: Any
    args = ... # type: Any
    def __init__(self, code, msg, sender) -> None: ...

class SMTPRecipientsRefused(SMTPException):
    recipients = ... # type: Any
    args = ... # type: Any
    def __init__(self, recipients) -> None: ...

class SMTPDataError(SMTPResponseException): ...
class SMTPConnectError(SMTPResponseException): ...
class SMTPHeloError(SMTPResponseException): ...
class SMTPAuthenticationError(SMTPResponseException): ...

def quoteaddr(addrstring): ...
def quotedata(data): ...

class SMTP:
    debuglevel = ... # type: Any
    file = ... # type: Any
    helo_resp = ... # type: Any
    ehlo_msg = ... # type: Any
    ehlo_resp = ... # type: Any
    does_esmtp = ... # type: Any
    default_port = ... # type: Any
    timeout = ... # type: Any
    esmtp_features = ... # type: Any
    source_address = ... # type: Any
    local_hostname = ... # type: Any
    def __init__(self, host=..., port=..., local_hostname=..., timeout=...,
                 source_address=...): ...
    def __enter__(self): ...
    def __exit__(self, *args): ...
    def set_debuglevel(self, debuglevel): ...
    sock = ... # type: Any
    def connect(self, host=..., port=..., source_address=...): ...
    def send(self, s): ...
    def putcmd(self, cmd, args=...): ...
    def getreply(self): ...
    def docmd(self, cmd, args=...): ...
    def helo(self, name=...): ...
    def ehlo(self, name=...): ...
    def has_extn(self, opt): ...
    def help(self, args=...): ...
    def rset(self): ...
    def noop(self): ...
    def mail(self, sender, options=...): ...
    def rcpt(self, recip, options=...): ...
    def data(self, msg): ...
    def verify(self, address): ...
    vrfy = ... # type: Any
    def expn(self, address): ...
    def ehlo_or_helo_if_needed(self): ...
    def login(self, user, password): ...
    def starttls(self, keyfile=..., certfile=..., context=...): ...
    def sendmail(self, from_addr, to_addrs, msg, mail_options=...,
                 rcpt_options=...): ...
    def send_message(self, msg, from_addr=..., to_addrs=..., mail_options=...,
                     rcpt_options=...): ...
    def close(self): ...
    def quit(self): ...

class SMTP_SSL(SMTP):
    default_port = ... # type: Any
    keyfile = ... # type: Any
    certfile = ... # type: Any
    context = ... # type: Any
    def __init__(self, host=..., port=..., local_hostname=..., keyfile=..., certfile=...,
                 timeout=..., source_address=..., context=...): ...

class LMTP(SMTP):
    ehlo_msg = ... # type: Any
    def __init__(self, host=..., port=..., local_hostname=..., source_address=...) -> None: ...
    sock = ... # type: Any
    file = ... # type: Any
    def connect(self, host=..., port=..., source_address=...): ...
