# Description
A package to make it easier to send email
# Usage
pip install easysendemail

send = SendEmail(sender=sender, receiver=receiver, smtp=smtp, port=port, password=password, subject=subject, filepath=filepth, filename=filename, content=content)

send.send_email()
