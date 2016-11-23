# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import os
import stripe
import random
from events import run, update
from flask import render_template, redirect, g, session
from flask import request, url_for, session, flash, make_response
from flask_user import login_required, roles_required, current_user
from flask_user.translations import gettext as _
from jinja2 import Environment, FileSystemLoader
from app.app_and_db import app, db
from app.users.models import UserAuth
from app.users.views import logout
from encryption import encode, decode
from operator import itemgetter
from date import *
from dateutil import *
from functions import weighted_choice, dollars
import json
from emails import *
import Queue
from events import *
from stripeErrorClass import stripeErrorClass
from calc import chartify

stripeErrors = stripeErrorClass()

### stripe ####################################
#app.config.from_pyfile('keys.cfg')
stripe_keys = {
    'secret_key': os.environ.get('STRIPE_SECRET_KEY')
    #'secret_key': app.config['SECRET_KEY']
}


## home pages and redirects ##################
@app.route('/', methods = ['GET'])
def home():
    return redirect(url_for('index'))

@app.route('/index', methods = ['GET'])
##@login_required
def index():
    #session.clear()
    if current_user.is_authenticated():
        # check to see if items are in session, this helps us to not make multiple API calls
        if 'api_key' in session:
            stripe.api_key = session['api_key']
        if 'events' in session:
            if len(session['events']) > 0:
                events = []
                for y in session['events'][0:19]:
                    x = json.loads(y)
                    p_date = pretty_date(x['dateint'])
                    event = Event(x['amount'],x['dateint'],x['date'],x['name'],x['type'],x['plan'],
                                  p_date,
                                  x['customer_id'])

                    events.append(event)

                current = session['current']
                per = session['percentages']
                churn = session['churn']
                ltv = session['ltv']

                return render_template('pages/index.html', events=events,mrr=current[0],refunds=current[1],net_revenue=current[2],
                                   annual=current[3],customers=current[4],new_customers=current[5], arpu=current[6],
                                   canceled=current[7],upgrades=current[8],downgrades=current[9],mrrP=per[0],refundsP=per[1],
                                   net_revenueP=per[2],annualP=per[3],customersP=per[4],new_customersP=per[5],arpuP=per[6],
                                   canceledP=per[7],upgradesP=per[8],downgradesP=per[9],churn=churn,ltv = ltv)
            else:
                clear_session() # clear the empty session
                events, current, per, churn, ltv = run()
                stripeErrors = returnErrors()
                if stripeErrors.AuthenticationError:
                    print stripeErrors.AuthenticationError
                    u = current_user.user_auth
                    u.credentials = 0
                    db.session.commit()
                    flash(_('Your API credentials were invalid, please enter them again.'), 'error')
                    return render_template('pages/getstarted.html')
                elif stripeErrors.APIConnectionError:
                    print stripeErrors.APIConnectionError
                    flash(_('Trouble connecting to Stripe. Please wait a minute and try again.'), 'error')
                    return render_template('pages/getstarted.html')
                else:
                    return render_template('pages/index.html', events=events,mrr=current[0],refunds=current[1],
                                           net_revenue=current[2],annual=current[3],customers=current[4],
                                           new_customers=current[5], arpu=current[6],canceled=current[7],
                                           upgrades=current[8],downgrades=current[9],mrrP=per[0],refundsP=per[1],
                                           net_revenueP=per[2],annualP=per[3],customersP=per[4],new_customersP=per[5],
                                           arpuP=per[6],canceledP=per[7],upgradesP=per[8],downgradesP=per[9],churn=churn,
                                           ltv = ltv)
        # otherwise make an api call
        else:
            events, current, per, churn, ltv = run()
            stripeErrors = returnErrors()
            if stripeErrors.AuthenticationError:
                print stripeErrors.AuthenticationError
                u = current_user.user_auth
                u.credentials = 0
                db.session.commit()
                flash(_('Your API credentials were invalid, please enter them again.'), 'error')
                return render_template('pages/getstarted.html')
            elif stripeErrors.APIConnectionError:
                print stripeErrors.APIConnectionError
                flash(_('Trouble connecting to Stripe. Please wait a minute and try again.'), 'error')
                return render_template('pages/getstarted.html')
            else:
                return render_template('pages/index.html', events=events,mrr=current[0],refunds=current[1],net_revenue=current[2],
                               annual=current[3],customers=current[4],new_customers=current[5], arpu=current[6],
                               canceled=current[7],upgrades=current[8],downgrades=current[9],mrrP=per[0],refundsP=per[1],
                               net_revenueP=per[2],annualP=per[3],customersP=per[4],new_customersP=per[5],arpuP=per[6],
                               canceledP=per[7],upgradesP=per[8],downgradesP=per[9],churn=churn,
                               ltv = ltv)
    else:
        #flash(_('Please login or signup to access this page.'), 'error')
        return render_template('pages/welcome.html')

@app.route('/data/<string:metric>', methods = ['GET'])
def data(metric):
    if 'events' in session:
        events = []
        for y in session['events']:
            x = json.loads(y)
            p_date = pretty_date(x['dateint'])
            event = Event(x['amount'],x['dateint'],x['date'],x['name'],x['type'],x['plan'],p_date,
                          x['customer_id'])
            events.append(event)

        dates, amounts = chartify(events, metric)
        metric = metric.replace("_", " ").title()
        return render_template('pages/data.html', metric=metric, dates=dates,amounts=amounts)
    else:
        return redirect(url_for('index'))

@app.route('/refresh')
@login_required
def refresh():
    if 'api_key' in session:
        stripe.api_key = session['api_key']
    clear_session()
    events, current, per, churn, ltv = update()
    return render_template('pages/index.html', events=events,mrr=current[0],refunds=current[1],net_revenue=current[2],
                           annual=current[3],customers=current[4],new_customers=current[5], arpu=current[6],
                           canceled=current[7],upgrades=current[8],downgrades=current[9],mrrP=per[0],refundsP=per[1],
                           net_revenueP=per[2],annualP=per[3],customersP=per[4],new_customersP=per[5],arpuP=per[6],
                           canceledP=per[7],upgradesP=per[8],downgradesP=per[9],churn=churn,ltv = ltv)

@app.route('/welcome')
def welcome():
    return render_template('pages/welcome.html')

##pricing and signup ##########################
@app.route('/getstarted', methods=['GET', 'POST'])
def getstarted():
    if current_user.is_authenticated():
        u = current_user.user_auth
        if u.credentials == 1:
            key = decode(u.api_key)
        else:
            key = " "
        if request.method=='POST':
            if request.form.get('key'):
                if (request.form.get('key').startswith('sk_live') or request.form.get('key').startswith('sk_test')) and \
                                len(request.form.get('key')) == 32:
                    u.api_key = encode(request.form.get('key'))
                    u.credentials = 1
                    session['api_key'] = request.form.get('key')
                    db.session.commit()

                    #flash(_('Successfully updated API credentials'), 'success')
                    stripe.api_key = session['api_key']
                    events, current, per, churn, ltv = run()
                    return render_template('pages/index.html', events=events,mrr=current[0],refunds=current[1],net_revenue=current[2],
                                   annual=current[3],customers=current[4],new_customers=current[5], arpu=current[6],
                                   canceled=current[7],upgrades=current[8],downgrades=current[9],mrrP=per[0],refundsP=per[1],
                                   net_revenueP=per[2],annualP=per[3],customersP=per[4],new_customersP=per[5],arpuP=per[6],
                                   canceledP=per[7],upgradesP=per[8],downgradesP=per[9],churn=churn,ltv = ltv)
                else:
                    u.credentials = 0
                    session['api_key'] = ""
                    db.session.commit()
                    flash(_('Your API credentials were invalid, please enter them again.'), 'error')
                    return render_template('pages/getstarted.html')
            else:
                flash(_('API credentials required.'), 'error')
                return render_template('pages/getstarted.html')

        return render_template('pages/getstarted.html', key=key)
    else:
        return redirect(url_for('user.login'))

@app.route('/pricing')
def pricing():
    if current_user.is_authenticated():
        return render_template('pages/plans.html')
    else:
        return render_template('pages/pricing.html')

@login_required
@app.route('/plans')
def plans():
    email=current_user.email
    return render_template('pages/plans.html', key=os.environ.get('PUBLISHABLE_KEY'), email=email)

@login_required
@app.route('/charge', methods=['POST'])
def charge():

    # Set the api key to Simple Metrics to create the customer and charge their card
    stripe.api_key = stripe_keys['secret_key']

    if current_user.is_authenticated():
        if current_user.user_auth.paying == 0:
            plan = request.form.get('plan')
            email = current_user.email

            customer = stripe.Customer.create(
                email=email,
                card=request.form['stripeToken']
            )

            # Create plan
            customer.subscriptions.create(plan=plan)

            # Write customer to db
            current_user.user_auth.customer = encode(customer.id)
            current_user.user_auth.paying = 1
            current_user.user_auth.plan = plan

            db.session.commit()

            send_welcome_email(email, plan.title())

            # Reset the stripe key
            stripe.api_key = ""

            flash(_('You have successfully signed up! Please enter your Stripe credentials below.'), 'success')
            return render_template('pages/getstarted.html')
        else:
            plan = request.form.get('plan')
            email = current_user.email

            #change the customer's plan
            customer = stripe.Customer.retrieve(decode(current_user.user_auth.customer))
            subscription = customer.subscriptions.retrieve(customer.subscriptions.data[0].id)
            subscription.plan = plan
            subscription.save()

            #update the db
            current_user.user_auth.plan = plan

            db.session.commit()

            flash(_('You have successfully switched to the ' + plan.title() + " plan."), 'success')
            send_plan_change_email(email, plan.title())

            # Reset the stripe key
            stripe.api_key = ""

            return render_template('pages/index.html')

    else:
        flash(_('Please login first.'), 'error')
        return render_template('pages/index.html')

@login_required
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    yes = url_for('delete_account')
    no = url_for('user_profile_page')
    flash(_('Are you sure you want to delete your account? This can\'t be undone. &nbsp;&nbsp;<a href="%(yes)s">Delete</a> '
            '&nbsp; <a href="%(no)s">Cancel</a>', yes=yes, no=no), 'error')
    return redirect('user/profile')

@login_required
@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if request.method=='GET':
        if current_user.is_authenticated():

            # Delete stripe subscription
            customer = stripe.Customer.retrieve(decode(current_user.user_auth.customer))
            customer.cancel_subscription()

            # delete user from database
            id = current_user.user_auth.id
            email = current_user.email
            user = UserAuth.query.filter_by(id=id).first()
            db.session.delete(user)
            db.session.delete(current_user)

            # commit database changes
            db.session.commit()

            #send the email
            send_cancel_email(email)
            flash(_('Your subscription has been successfully canceled.'), 'error')
            return logout()
        else:
            flash(_('Please login first.'), 'error')
            return render_template('pages/index.html')
    else:
        return redirect('/')

## data ################################
@app.route('/demo', methods = ['GET'])
def demo():
    return redirect('pages/index.html')

@login_required
@app.route('/dashboard', methods = ['GET'])
def dashboard():
    """
    if current_user.is_authenticated():
        if current_user.user_auth.paying == 1:
            if current_user.user_auth.credentials == 0:
                flash(_('Please enter API credentials to view your dashboard.'), 'error')
                return render_template('pages/getstarted.html')
            elif current_user.user_auth.credentials == -1:
                flash(_('Your PayPal credentials are invalid. Please enter them again.'), 'error')
                return render_template('pages/getstarted.html')
            else:
                transactions = sorted(return_transactions(), key=itemgetter('date'), reverse=True)

                payments, mrr, refunds, num_customers, customers, run_rate, arpu, fees = get_data(return_transactions())

                failed, prior_failed = return_failed_count()

                payments_percent, mrr_percent, refunds_percent, num_customers_percent, run_rate_percent, arpu_percent, \
                fees_percent, failed_percent = get_percentages()
                user_churn = get_user_churn()

                return render_template('pages/dashboard.html', transactions_list = transactions, net_revenue = payments,
                                       net_revenue_percent = payments_percent, mrr = mrr, mrr_percent = mrr_percent,
                                       refunds = refunds, refunds_percent = refunds_percent, run_rate = run_rate,
                                       run_rate_percent = run_rate_percent, customers = num_customers, customers_percent =
                                       num_customers_percent, user_churn = user_churn, annual_percent = 0, fees = fees,
                                       fees_percent = fees_percent, arpu = arpu, arpu_percent = arpu_percent,
                                       failed = failed, failed_percent = failed_percent)
        else:
            email = current_user.email
            flash(_('You must sign up for a plan first.'), 'error')
            return render_template('pages/plans.html', key=stripe_keys['publishable_key'], email=email)
    else:
    """
        #flash(_('Please login first.'), 'error')
    return redirect('pages/index.html')

## contact ######################################
@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if request.method=='POST':
        if current_user.is_authenticated():
            email = current_user.email
        else:
            email = ""

        message = request.form.get('message')
        contact_us_email(email, message)

        flash(_('Your email has been successfully sent! We\'ll get back to you as soon as possible.'), 'success')
        return render_template('pages/contact_us.html', email = email, message = message)
    else:
        return render_template('pages/contact_us.html')

## other pages ###################################
# The home page is the same as /
@app.route('/home_page')
def home_page():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    else:
        return redirect('pages/welcome.html')

@app.route('/member')
@login_required             # Limits access to authenticated users
def member_page():
    return render_template('pages/member_page.html')

# The Admin page is accessible to users with the 'admin' role
@app.route('/admin')
@roles_required('admin')    # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')

@app.route('/gallery', methods = ['GET'])
def gallery():
    return render_template('pages/gallery.html', run_rate=2700)

@app.route('/portfolio')
def portfolio():
    return render_template('pages/portfolio.html')


## error handling ##################################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404

@app.errorhandler(Exception)
def handle_bad_request(e):
    return render_template('pages/404.html'), 404
