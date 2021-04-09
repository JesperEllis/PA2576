import smtplib
import ssl
import random
import string

class MailSender:
    def __init__(self):
        """attributes needed for SMTP server"""
        self._port = 465
        self._sender = "stockfluentinfo@gmail.com"
        self._password = "pa2576student"
        self._context = ssl.create_default_context()
        self._code_generator = CodeGenerator()

    def reset_password(self, receiver):
        """
        Entry method for flask script to request reset password functionality
        Currently the method does not know about tha DatabaseInterface and
        therfore needs receiver email as parameter!!
        
        """
        code = self._code_generator.generate_code()
        #skicka med länk
        message = "Subject: Reset Password" + '\n\n' + f'A request to reset password on your account has been made! \n\nEnter the following code to choose a new password.\nYour code: {code}'
        
        try:
            self._send_email(receiver, message=message)
        except Exception:
            return "Email does not exsist"
        return code

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

class CodeGenerator:
    def generate_code(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

if __name__ == '__main__':
    ms = MailSender()
    ms.reset_password('elion.eriksson@hotmail.com')