__author__ = 'Ricky'
from flask import Flask, render_template
from flask_mail import Mail, Message

#*** Remember to change the email sender at production time! ***

def send_welcome_email(email, plan):
    app = Flask(__name__)
    mail = Mail()
    mail.init_app(app)
    msg = Message("You've successfully signed up for SimpleMetrics!",
                  sender="rickycharpentier@gmail.com",
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
                  sender="rickycharpentier@gmail.com",
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
                  recipients=["rickycharpentier@gmail.com"],
                  sender="rickycharpentier@gmail.com")
    msg.body = email + " sent you a message:\n\n" + message

    mail.send(msg)

def send_cancel_email(email):
    app = Flask(__name__)
    mail = Mail()
    mail.init_app(app)
    msg = Message("Goodbye from SimpleMetrics",
                  sender="rickycharpentier@gmail.com",
                  recipients=[email])

    msg.html = render_template('pages/cancel_email.html')

    mail.send(msg)
