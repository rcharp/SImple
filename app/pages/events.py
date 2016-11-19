__author__ = 'Ricky'

import stripe
from flask import session
import time
from date import *
from eventClass import Event
import threading
import Queue
from calc import calculate, chartify
import inspect
from flask_cache import Cache
from flask_user import current_user
from app.app_and_db import app
from stripeErrorClass import stripeErrorClass

app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)
stripeError = stripeErrorClass()

event_types = ["charge.failed", "charge.refunded", "charge.succeeded","customer.subscription.created","customer.subscription.deleted", "customer.subscription.updated"]

eventList = []
eventQueue = Queue.Queue()
apiQueue = Queue.Queue()
callQueue = Queue.Queue()

class eventThread(threading.Thread):
    def __init__(self, queue, list):
        threading.Thread.__init__(self)
        self.queue = queue
        self.list = list

    def run(self):
        while True:
            event = self.queue.get()
            process(event, self.list)
            self.queue.task_done()

class apiThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            dates = self.queue.get()
            call(dates)
            self.queue.task_done()

# processes each item from the api call and puts it into a list that will be passed to the dashboard later.
def process(item, list):

    if item.type in event_types:
        event = Event() # create an Event() object to hold each item's data
        if item.type == "customer.subscription.updated":
            if 'plan' in item.data.previous_attributes:
                if item.data.previous_attributes.plan.amount < item.data.object.plan.amount:
                    event.type = "Upgrade"
                else:
                    event.type = "Downgrade"
                #customer = stripe.Customer.retrieve(item.data.object.customer)
                #item.name = customer.sources.data[0].name[:5].title()
                event.name = "Ricky"
                event.amount = 0
                event.plan = item.data.object.plan.name
                event.customer_id = item.data.object.customer
                event.dateint = item.created
                event.date = get_date_string(event.dateint)
                event.p_date = pretty_date(event.dateint)
                list.append(event)
        elif item.type in ("customer.subscription.deleted", "customer.subscription.created"):
            #customer = stripe.Customer.retrieve(item.data.object.customer)
            #item.name = customer.sources.data[0].name[:5].title()
            if item.type == "customer.subscription.deleted":
                event.dateint = item.data.object.canceled_at
            else:
                event.dateint = item.created
            event.name = "Jermaine"
            event.amount = 0
            event.customer_id = item.data.object.customer
            event.date = get_date_string(event.dateint)
            event.type = item.type
            event.p_date = pretty_date(event.dateint)
            event.plan = item.data.object.plan.name
            list.append(event)
        else:
            if item.type == "charge.refunded":
                event.amount = -(float(item.data.object.amount_refunded))/100
            else:
                event.amount = float(item.data.object.amount)/100
            #item.name = item.data.object.card.name[:5].title()
            event.name = "Ophenson"
            event.customer_id = item.data.object.card.customer
            event.dateint = item.created
            event.date = get_date_string(event.dateint)
            event.p_date = pretty_date(event.dateint)
            event.type = item.type
            list.append(event)


# do the API call to stripe, using multiple threads. also checks for API errors.
def call(dates, last=None):
    stripeError.destroy()
    try:

        start_date = dates[0]
        end_date = dates[1]
        apiCall = stripe.Event.list(created={'gte':start_date, 'lte':end_date}, limit = 300, starting_after=last)

        if apiCall.has_more == True:
            last = apiCall.data[-1]
            call(dates, last)

        for x in apiCall:
            eventQueue.put(x)

        for i in range(10):
            thread = eventThread(eventQueue, eventList)
            thread.setDaemon(True)
            thread.start()

        eventQueue.join()
    except stripe.error.AuthenticationError as error:
        stripeError.AuthenticationError = error
    except stripe.error.APIConnectionError as error:
        stripeError.APIConnectionError = error

# returns a list of any errors from the API call
def returnErrors():
    return stripeError

# used by multiple threads to do several API calls at one time.
#@app.cache.cached(timeout=1200, key_prefix='events')
def run():

    del eventList[:]
    now = datetime.datetime.now()
    one_month_ago = now - datetime.timedelta(days=31)
    two_months_ago = now - datetime.timedelta(days=60)

    current = (one_month_ago, now)
    previous = (two_months_ago, one_month_ago)

    apiQueue.put(current)
    apiQueue.put(previous)

    for i in range(2):
        thread = apiThread(apiQueue)
        thread.setDaemon(True)
        thread.start()

    apiQueue.join()

    # clear out the session's cache before we calculate
    clear_session()

    return calculate(eventList)

# runs when the user clicks Update on the live transactions box. bypasses the session/cache and runs another, more
# current api call
def update():
    del eventList[:]
    now = datetime.datetime.now()
    one_month_ago = now - datetime.timedelta(days=31)
    two_months_ago = now - datetime.timedelta(days=60)

    current = (one_month_ago, now)
    previous = (two_months_ago, one_month_ago)

    apiQueue.put(current)
    apiQueue.put(previous)

    for i in range(2):
        thread = apiThread(apiQueue)
        thread.setDaemon(True)
        thread.start()

    apiQueue.join()

    # clear out the cache
    clear_session()

    return calculate(eventList)

def clear_session():
    # clear out the session's cache before we calculate
    for item in ('events', 'current', 'per', 'churn', 'ltv'):
        if item in session:
            del session[item]