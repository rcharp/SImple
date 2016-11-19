__author__ = 'Ricky'

import stripe
from date import one_month_ago, now, yesterday, twenty_four_months_ago

stripe.api_key = 'sk_test_aPce5SASjjzwyGWHlokJUOqt'
events_list = []
event_types = ["charge.failed", "charge.refunded", "charge.succeeded", "customer.subscription.created",
         "customer.subscription.deleted", "customer.subscription.updated"]

def list_events(last=None, count=0):
    limit = 15
    events = stripe.Event.list(created={'gte':twenty_four_months_ago, 'lte':now}, limit=limit, starting_after=last)
    event=0
    while events is not None:
        try:
            if count == limit:
                break
            if events.data[event]['type'] in event_types:
                if events.data[event]['type'] == "customer.subscription.updated":
                    if 'plan' in events.data[event]['data']['previous_attributes']:
                        print events.data[event]
                        print "---------------"
                        #events_list.append(events.data[event])
                        count += 1
                else:
                    print events.data[event]
                    print "---------------"
                    #events_list.append(events.data[event])
                    count += 1
            event += 1
        except IndexError:
            if events.has_more == False:
                break
            else:
                list_events(events.data[event-1], count)
            break
        except KeyError:
            break

    #return events_list

def clear_events():
    del events_list[:]

list_events()