__author__ = 'Ricky'
from flask import Flask, render_template
from flask_mail import Mail, Message

#*** Remember to change the email sender at production time! ***

def send_welcome_email(email, plan):
    app = Flask(__name__)
    mail = Mail()
    mail.init_app(app)
    msg = Message("You've successfully signed up for SimpleMetrics!",
                  #sender="support@getsimplemetrics.com",
                  sender="getsimplemetrics@gmail.com",
                  recipients=[email])
    if (plan == 'Hobby'):
        amount = 39
    elif (plan == 'Startup'):
        amount = 79
    else:
        amount = 149
    msg.html = render_template('pages/welcome_email.html', plan=plan, amount=amount)

    mail.send(msg)

def send_plan_change_email(email, plan):
    app = Flask(__name__)
    mail = Mail()
    mail.init_app(app)
    msg = Message("Your plan with SimpleMetrics has been changed.",
                  #sender="support@getsimplemetrics.com",
                  sender="simplemetrics@gmail.com",
                  recipients=[email])
    if (plan == 'Hobby'):
        amount = 39
    elif (plan == 'Startup'):
        amount = 79
    else:
        amount = 149
    msg.html = render_template('pages/plan_change_email.html', plan=plan, amount=amount)

    mail.send(msg)

def contact_us_email(email, message):
    app = Flask(__name__)
    mail = Mail()
    mail.init_app(app)
    msg = Message("Support request from " + email,
                  #recipients=["support@getsimplemetrics.com"],
                  recipients=["getsimplemetrics@gmail.com"],
                  #sender="support@getsimplemetrics.com")
                  sender="getsimplemetrics@gmail.com")
    msg.body = email + " sent you a message:\n\n" + message

    response = Message("Your email to SimpleMetrics has been received.",
                       recipients=[email],
                       sender="donotreply@getsimplemetrics.com")

    response.body = "\n\nThanks for emailing us! Your message has been sent and we'll reply shortly. Please don't " \
                    "respond to this email, as it's coming from an autoresponder and we won't get any replies to " \
                    "this address.\n\nThe email address you provided is " + email + "."

    mail.send(msg)
    mail.send(response)

def send_cancel_email(email):
    app = Flask(__name__)
    mail = Mail()
    mail.init_app(app)
    msg = Message("Goodbye from SimpleMetrics",
                  #sender="support@getsimplemetrics.com",
                  sender="getsimplemetrics@gmail.com",
                  recipients=[email])

    msg.html = render_template('pages/cancel_email.html')

    mail.send(msg)
