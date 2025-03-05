from flask_mail import Mail, Message
from Utils.helper import create_response


mail = Mail()

def init_mail(app):
    """Initialize the mail instance with the Flask app."""
    mail.init_app(app)

def send_mail(recipients,subject,html_template,sender):
    msg = Message(subject,
                      recipients=[recipients],
                      sender=sender,
                      html=html_template)  # Include the HTML content here
    mail.send(msg)
    return create_response(True,"Mail sent successfully",None,None)