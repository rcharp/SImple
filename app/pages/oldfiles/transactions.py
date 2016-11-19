__author__ = 'Ricky'

import stripe
from date import now, yesterday, one_week_ago, three_months_ago, twelve_months_ago, twenty_four_months_ago, \
    three_days_ago, one_month_ago, get_date_string, get_datetime_string, pretty_date, get_datetime
from app.pages.oldfiles import api
from functions import dollars

list = []

"""
def list_all_charges(last=None):
    limit = 1000
    charges = stripe.Charge.all(created={'gte':twenty_four_months_ago, 'lte':now}, limit=limit, starting_after=last)
    charge=0
    while charges is not None:
        try:
            if charge == limit:
                break
            #print "Charge number: " + str(charge) + " Amount: $" + str(charges.data[charge]['amount'])
            #print charges.data
            if charges.data[charge]['refunded'] == True:
                list.append({'amount':dollars(charges.data[charge]['amount']),
                             'date':get_date_string(charges.data[charge]['created']),
                             'card':charges.data[charge]['card']['last4'],
                             'name':charges.data[charge]['card']['name'],
                             'email':charges.data[charge]['receipt_email'],
                             'type': "Refund",
                             'status':charges.data[charge]['status'].title()
                })
            else:
                list.append({'amount':dollars(charges.data[charge]['amount']),
                             'date':get_date_string(charges.data[charge]['created']),
                             'card':charges.data[charge]['card']['last4'],
                             'name':charges.data[charge]['card']['name'],
                             'email':charges.data[charge]['receipt_email'],
                             'type': "Payment",
                             'status':charges.data[charge]['status'].title()
                })
            charge += 1
        except IndexError:
            if charges.has_more == False:
                print ("ALL CHARGES LISTED SUCCESSFULLY")
                break
            else:
                list_all_charges(charges.data[charge-1])
            break
        except KeyError:
            print "keyerror"
    return list
"""
def list_charges(last=None):
    limit = 15
    charges = stripe.Charge.all(created={'gte':one_month_ago, 'lte':now}, limit=limit, starting_after=last)
    charge=0
    while charges is not None:
        try:
            if charge == limit:
                break
            #print "Charge number: " + str(charge) + " Amount: $" + str(charges.data[charge]['amount'])
            #print charges.data
            if charges.data[charge]['refunded'] == True:
                list.append({'amount':dollars(charges.data[charge]['amount']),
                             'dollar_amount':(charges.data[charge]['amount'])/100,
                             'date':get_date_string(charges.data[charge]['created']),
                             'true_date':charges.data[charge]['created'],
                             'p_date':pretty.date(get_datetime(charges.data[charge]['created'])),
                             'card':charges.data[charge]['card']['last4'],
                             'name':charges.data[charge]['card']['customer'],
                             'email':charges.data[charge]['receipt_email'],
                             'type': "Refund",
                             'status':charges.data[charge]['status'].title()
                })
            else:
                list.append({'amount':dollars(charges.data[charge]['amount']),
                             'dollar_amount':(charges.data[charge]['amount'])/100,
                             'date':get_date_string(charges.data[charge]['created']),
                             'true_date':charges.data[charge]['created'],
                             'p_date':pretty.date(get_datetime(charges.data[charge]['created'])),
                             'card':charges.data[charge]['card']['last4'],
                             'name':charges.data[charge]['card']['customer'],
                             'email':charges.data[charge]['receipt_email'],
                             'type': "Payment",
                             'status':charges.data[charge]['status'].title()
                })
            #print charges.data[charge]
            charge += 1
        except IndexError:
            if charges.has_more == False:
                break
            else:
                list_charges(charges.data[charge-1])
            break
        except KeyError:
            print "keyerror"

    return list

def clear_transactions():
    del list[:]

#new_list = list_all_charges()

#for item in new_list:
    #print(str(item))

#print len(new_list)

#list_charges()