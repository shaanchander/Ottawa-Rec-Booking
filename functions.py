import email
import imaplib
from datetime import datetime
from time import sleep
from config import *


# https://github.com/medsagou/Read-email-from-gmail-inbox-using-python
def getGmailCode(sentTime):

    host = "imap.gmail.com"

    # Create server and login
    mail = imaplib.IMAP4_SSL(host)
    mail.login(user, gmail_pass)

    for attempts in range(30):

        print(f'\nAttempt {attempts} to fetch code')

        # Using SELECT to chose the e-mails.
        res, messages = mail.select('INBOX')

        # Caluclating the total number of sent Emails
        messages = int(messages[0])

        # Iterating over the sent emails
        for i in range(messages, messages - 1, -1):
            # RFC822 protocol
            res, msg = mail.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # print(response[1])
                    msg = email.message_from_bytes(response[1])

                    print(msg['Date'])
                    # make date of email reception into datetime obj
                    receivedTime = datetime.strptime(msg['Date'].replace(' (UTC)', ''), "%a, %d %b %Y %H:%M:%S %z")
                    # print(receivedTime)
                    # input()

                    # print(sentTime)
                    # print(receivedTime)

                    deltaSeconds = (receivedTime - sentTime).total_seconds()

                    # input()

                    # Store the senders email
                    sender = msg["From"]

                    # Store subject of the email
                    subject = msg["Subject"]

                    print(f'email delta: {deltaSeconds}')
                    # input()

                    if 'noreply@frontdesksuite.com' not in sender or subject != 'Verify your email' or deltaSeconds > 30 or deltaSeconds < 0:
                        sleep(1)
                        continue

                    # Store Body
                    body = ""
                    temp = msg
                    if temp.is_multipart():
                        for part in temp.walk():
                            ctype = part.get_content_type()
                            cdispo = str(part.get('Content-Disposition'))

                            # skip text/plain type
                            if ctype == 'text/plain' and 'attachment' not in cdispo:
                                body = part.get_payload(decode=True)  # decode
                                break
                    else:
                        body = temp.get_payload(decode=True)

                    body = str(body)
                    code = body.split('Your verification code is:\\r\\n')[1].split('.')[0]
                    # print(code)
                    # print(datetime.now())

                    mail.close()
                    mail.logout()

                    return code

    # Close the connection.
    mail.close()
    mail.logout()

    return -1
