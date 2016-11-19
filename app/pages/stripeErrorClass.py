__author__ = 'Ricky'

class stripeErrorClass():
    def __init__(self):
        self.AuthenticationError = ""
        self.APIConnectionError = ""
        self.errors = []

    def destroy(self):
        self.AuthenticationError = ""
        self.APIConnectionError = ""
        self.errors = []
