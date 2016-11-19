__author__ = 'Ricky'

import stripe
import time
import threading
from date import three_months_ago, now
import eventClass

stripe.api_key = 'sk_test_aPce5SASjjzwyGWHlokJUOqt'

event_types = ["charge.failed", "charge.refunded", "charge.succeeded", "customer.subscription.created",
             "customer.subscription.deleted", "customer.subscription.updated"]
limit = 15
newlist = []

class myThread(threading.Thread):
    def __init__(self, start, end, list):
        threading.Thread.__init__(self)
        self.start_time = start
        self.end = end

    def run(self, events, list):
        process(events, self.start_time, self.end, list)

def process(events, start, end, list):
    event = eventClass.Event()
    for item in events[start:end]:
        if item['type'] in event_types:
            if item['type'] == "customer.subscription.updated":
                if 'plan' in item.data['data']['previous_attributes']:
                    if item.data['data']['previous_attributes']['plan']['amount'] < item.data['data']['object']['plan']['amount']:
                        item.type = "Upgrade"
                    else:
                        item.type = "Downgrade"
                    customer = stripe.Customer.retrieve(events.data['data']['object']['customer'])
                    item.name = customer.sources['data'][0]['name'][:5].title()
                    item.plan = events.data[count]['data']['object']['plan']['name']
                    item.date = events.data[count]['created']
                    list.append(item)
            elif item['type'] in ("customer.subscription.deleted", "customer.subscription.created"):
                customer = stripe.Customer.retrieve(events.data['data']['object']['customer'])
                item.name = customer.sources['data'][0]['name'][:5].title()
                item.type = events.data['type']
                item.date = events.data['created']
                item.plan = events.data['data']['object']['plan']['name']
                list.append(item)
            else:
                item.name = events.data['data']['object']['card']['name'][:5].title()
                item.amount = (events.data['data']['object']['amount'])/100
                item.date = events.data['created']
                item.type = events.data['type']
                list.append(item)

start = time.time()
events = list(stripe.Event.list(created={'gte':three_months_ago, 'lte':now}, limit = 50))

print events

end = time.time()


print newlist

print "time is " + str(end - start)
