from date import one_month_ago, now, two_months_ago, get_datetime_string, get_datetime, get_date_string, get_short_date_string, \
    datetime_to_int, \
                                                         yesterday, jsonify
from flask_cache import Cache
from flask import session
from app.app_and_db import app
from collections import OrderedDict, Counter
from eventClass import Event
import datetime
import json

app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)

# used for the percentages of each metric
def convert_to_percent(value):
    value = value * 100
    value = float("{:.1f}".format(float(value)))
    return value

# all the metrics calculations are done here
#@app.cache.cached(timeout=600, key_prefix='calculations')
def calculate(list):
    # sort list by date integer in order to get transactions in right order
    list.sort(key=lambda  x: x.dateint, reverse=True)

    # transaction calcuations

    mrr = sum(x.amount for x in list if get_datetime(x.dateint) >= one_month_ago and x.type in
              ("charge.succeeded","charge.refunded") and len([y for y in list if y.type in
              ("charge.succeeded","charge.refunded") and y.customer_id == x.customer_id]) > 1)
    prev_mrr = sum(x.amount for x in list if get_datetime(x.dateint) < one_month_ago and x.type in
                   ("charge.succeeded","charge.refunded") and len([y for y in list if y.type in
                   ("charge.succeeded","charge.refunded") and y.customer_id == x.customer_id]) > 1)
    canceled = len(set([x.customer_id for x in list if x.type == "customer.subscription.deleted"
                         and get_datetime(x.dateint) >= one_month_ago]))
    upgrades = len([x for x in list if x.type == "Upgrade" and get_datetime(x.dateint) >= one_month_ago])
    prev_upgrades = len([x for x in list if x.type == "Upgrade" and get_datetime(x.dateint) < one_month_ago])
    downgrades = len([x for x in list if x.type == "Downgrade" and get_datetime(x.dateint) >= one_month_ago])
    prev_downgrades = len([x for x in list if x.type == "Downgrade" and get_datetime(x.dateint) < one_month_ago])
    prev_canceled = len(set([x.customer_id for x in list if x.type == "customer.subscription.deleted"
                         and get_datetime(x.dateint) < one_month_ago]))
    refunds = sum(x.amount for x in list if x.type == "charge.refunded" and get_datetime(x.dateint) >= one_month_ago)
    prev_refunds = sum(x.amount for x in list if x.type == "charge.refunded" and get_datetime(x.dateint) < one_month_ago)
    net_revenue = sum(x.amount for x in list if get_datetime(x.dateint) >= one_month_ago and x.type in
                      ("charge.succeeded","charge.refunded"))
    prev_net_revenue = sum(x.amount for x in list if get_datetime(x.dateint) < one_month_ago and x.type in
                      ("charge.succeeded","charge.refunded"))

    annual = mrr * 12
    prev_annual = prev_mrr * 12

    customers = len(set([x.customer_id for x in list if get_datetime(x.dateint) >= one_month_ago]))
    prev_customers = len(set([x.customer_id for x in list if get_datetime(x.dateint) < one_month_ago]))

    new_customers = len(set([x.customer_id for x in list if x.type == "customer.subscription.created"
                             and get_datetime(x.dateint) >= one_month_ago]))
    prev_new_customers = len(set([x.customer_id for x in list if x.type == "customer.subscription.created"
                             and get_datetime(x.dateint) < one_month_ago]))

    arpu = ((float(mrr) / customers) if customers != 0 else 0)
    prev_arpu = ((prev_mrr / prev_customers) if prev_customers != 0 else 0)

    #save the events list in session, so that we don't have to do an api call every time.
    eventsList = []
    for x in list:
        y = json.dumps(x.__dict__)
        eventsList.append(y)

    # cut the list down for the live transactions on main dashboard
    del list[19:]

    # calculate churn and ltv
    churn = (((float(canceled) / prev_customers) * 100) if prev_customers != 0 else 0)
    ltv = ((arpu / churn) * 100 if churn != 0 else 0)

    # the metrics that we are going to be sending to the dashboards to occupy metric tiles
    current = (mrr, refunds, net_revenue, annual, customers, new_customers, arpu, canceled, upgrades, downgrades)
    prev = (prev_mrr, prev_refunds, prev_net_revenue, prev_annual, prev_customers, prev_new_customers, prev_arpu,
            prev_canceled, prev_upgrades, prev_downgrades)
    percentages = [convert_to_percent((x - y) / float(y)) if y != 0 else convert_to_percent(0) for x, y in zip(current,prev)]

    # add results to the session to avoid multiple calls to the API
    session['events'] = eventsList
    session['current'] = current
    session['percentages'] = percentages
    session['churn'] = churn
    session['ltv'] = ltv

    #print "just put events into the session"
    #print session['events']

    return list, current, percentages, churn, ltv



# gets the dates and the amounts for the chart for each metric to be displayed.
#@app.cache.cached(timeout=600, key_prefix='charts')
def chartify(events, metric):

    d = OrderedDict()
    dates = []
    amounts = []

    data = sorted(events, key=lambda x: x.dateint)
    #data = [x for x in data if get_datetime(x.dateint) >= one_month_ago and x.type in ("charge.succeeded",
    # "charge.refunded")]

    if 'net' in metric:
        data = [x for x in data if get_datetime(x.dateint) >= one_month_ago and x.type in ("charge.succeeded", "charge.refunded")]
    elif 'monthly' in metric:
        data = [x for x in data if get_datetime(x.dateint) >= one_month_ago and x.type in ("charge.succeeded","charge.refunded") and len([y for y in data if y.type in ("charge.succeeded","charge.refunded") and y.customer_id == x.customer_id]) > 1]
    elif 'annual' in metric:
        print
    elif 'average' in metric:
        print
    elif 'total' in metric:
        data = len(set([x.customer_id for x in list if get_datetime(x.dateint) >= one_month_ago]))
    elif 'refunds' in metric:
        print
    elif 'churn' in metric:
        print
    elif 'lifetime' in metric:
        print
    elif 'new' in metric:
        data = [x for x in data]
    elif 'canceled' in metric:
        print
    elif 'upgrades' in metric:
        print
    elif 'downgrades' in metric:
        print

    if len(data) == 0:
        dates.append(yesterday.strftime("%B %d"))
        amounts.append(0)

        dates.append(now.strftime("%B %d"))
        amounts.append(0)
    elif len(data) == 1:
        dates.append((get_datetime(data[0].dateint) - datetime.timedelta(days=7)).strftime("%B %d"))
        amounts.append(0)

        dates.append(get_short_date_string(data[0].dateint))
        amounts.append(data[0].amount)

        if get_short_date_string(data[0].dateint) != now.strftime("%B %d"):
            dates.append(now.strftime("%B %d"))
            amounts.append(0)
    else:
        for item in data:
            key = get_short_date_string(item.dateint)
            if key not in d:
                d[key] = []
            d[key].append(item.amount)

        for k, v in d.items():
            dates.append(k)
            amounts.append(sum(v))

    #session['dates'] = dates
    #session['amounts'] = amounts

    return dates, amounts
