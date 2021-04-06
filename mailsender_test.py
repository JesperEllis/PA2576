import smtplib
import ssl

# user_emails = ["elion.eriksson@hotmail.com"]



class MailSender:
    def __init__(self):
        """attributes needed for SMTP server"""
        self._port = 465
        self._sender = "stockfluentinfo@gmail.com"
        self._password = "pa2576student"
        self._context = ssl.create_default_context()

    def reset_password(self, receiver):
        """
        Entry method for flask script to request reset password functionality
        Currently the method does not know about tha DatabaseInterface and
        therfore needs receiver email as parameter!!
        
        """
        #skicka med länk
        message = "Subject: Reset Password" + '\n\n' + f'{receiver}'
        try:
            self._send_email(receiver, message=message)
        except Exception:
            return "Email does not exsist"
        return "successfull"

    def send_recommendation(self, receiver):
        """
        Entry method for flask script to request reset password functionality
        Currently the method does not know about tha DatabaseInterface and
        therfore needs receiver email as parameter!!
        
        """
        message = "Subject: New Recommendation" + '\n\n' + f'{receiver}'
        self._send_email(receiver, message=message)

        
    
    def _send_email(self, receiver, message):
        with smtplib.SMTP_SSL("smtp.gmail.com", self._port, context=self._context) as server:
            try:
                server.login(self._sender, self._password)
                server.sendmail(self._sender, receiver, message)
                print("Successfully sent mail!")
            except Exception:
                return "Falut"

if __name__ == '__main__':
    ms = MailSender()
    ms.send_email("elion.eriksson@hotmail.com")