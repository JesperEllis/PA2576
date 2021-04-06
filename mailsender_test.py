import smtplib
import ssl

# user_emails = ["elion.eriksson@hotmail.com"]



class MailSender:
    def __init__(self):
        self._port = 465
        self._sender = "stockfluentinfo@gmail.com"
        self._password = "pa2576student"
        self._context = ssl.create_default_context()

    def reset_password(self, receiver):
        #skicka med länk
        message = "Subject: Reset Password" + '\n\n' + f'{receiver}'
        self._send_email(receiver, message=message)

    def send_recommendation(self, receiver):
        message = "Subject: New Recommendation" + '\n\n' + f'{receiver}'
        self._send_email(receiver, message=message)
    
    def _send_email(self, receiver, message):
        with smtplib.SMTP_SSL("smtp.gmail.com", self._port, context=self._context) as server:
            try:
                server.login(self._sender, self._password)
            except:
                raise "Det gick inte att logga in"
            server.sendmail(self._sender, receiver, message)
            print("Successfully sent mail!")


ms = MailSender()
ms.send_email("elion.eriksson@hotmail.com")