__author__ = 'Ricky'

from date import datetime_to_int
from random import randint
import datetime

def random_date(start, end):
    return start + datetime.timedelta(seconds=randint(0, int((end - start).total_seconds())))

types = ["charge.failed", "charge.refunded", "charge.succeeded","customer.subscription.created","customer.subscription.deleted", "Upgrade", "Downgrade"]

names = ["Someone", "Somebody", "A Customer", "A Company", "Someone Else", "Another Customer"]

plans = ["SimpleMetrics Hobby Plan", "SimpleMetrics Startup Plan", "SimpleMetrics Professional Plan"]

amounts = [39, 79, 149]