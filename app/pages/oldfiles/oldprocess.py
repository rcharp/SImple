__author__ = 'Ricky'

def process(item, list):
    event = eventClass.Event()
    if item['type'] in event_types:
        if item['type'] == "customer.subscription.updated":
            if 'plan' in item['data']['previous_attributes']:
                if item['data']['previous_attributes']['plan']['amount'] < item['data']['object']['plan']['amount']:
                    event.type = "Upgrade"
                else:
                    event.type = "Downgrade"
                #customer = stripe.Customer.retrieve(item['data']['object']['customer'])
                #event.name = customer.sources['data'][0]['name'][:5].title()
                event.name = "Ricky"
                event.plan = item['data']['object']['plan']['name']
                event.date = item['created']
                event.clean_date = get_datetime(event.date)
                event.p_date = pretty_date(event.date)
                list.append(event)
        elif item['type'] in ("customer.subscription.deleted", "customer.subscription.created"):
            #customer = stripe.Customer.retrieve(item['data']['object']['customer'])
            #event.name = customer.sources['data'][0]['name'][:5].title()
            event.name = "Jermaine"
            event.type = item['type']
            event.date = item['created']
            event.clean_date = get_datetime(event.date)
            event.p_date = pretty_date(event.date)
            event.plan = item['data']['object']['plan']['name']
            list.append(event)
        else:
            if item['type'] == "charge.refunded":
                event.amount = -(item['data']['object']['amount_refunded'])/100
            else:
                event.amount = (item['data']['object']['amount'])/100
            #event.name = item['data']['object']['card']['name'][:5].title()
            event.name = "Ophenson"
            event.date = item['created']
            event.clean_date = get_datetime(event.date)
            event.p_date = pretty_date(event.date)
            event.type = item['type']
            list.append(event)
