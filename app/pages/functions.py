#from api_calls import return_transactions, return_prior_transactions, return_failed_count
from bisect import bisect
from flask import Flask, render_template
import random
import decimal

def convert_to_percent(value):
    value = value * 100
    value = float("{:.1f}".format(float(value)))
    return value

def weighted_choice(choices):
    values, weights = zip(*choices)
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random.random() * total
    i = bisect(cum_weights, x)
    return values[i]

def dollars(amount):
    amount = "${:,.2f}".format(decimal.Decimal(float(amount)) / 100)
    return amount