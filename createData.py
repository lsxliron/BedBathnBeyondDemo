"""
    This file fills the database with synthetic data
"""
from demo.models import Transaction, Store
import datetime
import random

def createStores(numOfStores):
    """
        Fills the stores table

        :param numOfStores: The number of random stores to create
        :type numOfStores: int
    """
    states = ['NY', 'NJ', 'CT', 'PA', 'MA']
    
    # Create 100 random stores
    for i in xrange(numOfStores):
        s = Store()
        stateChoice = random.randint(0,len(states)-1)
        s.state = states[stateChoice]
        s.numOfEmployees = random.randint(50, 500)
        s.expenses = random.randint(1000, 10000)
        s.size = random.randint(100, 2000)
        s.save()


def createTransactions(numOfTransactions):
    """
        Fills the transactions table
        
        :param numOfTransactions: The number of random transactions to create
        :type numOfTransactions: int
    """
    for i in xrange(numOfTransactions):
        t = Transaction()
        t.amount = random.random()*1000
        day = random.randint(1,28)
        month = random.randint(1, 12)
        t.date = datetime.date(2015, month, day)

        storeChoice = random.randint(0,len(Store.objects.all())-1)
        t.store = Store.objects.all()[storeChoice]

        t.save()        

def main():
    createStores(100)
    createTransactions(5000)
    # fillStores()
    # fillTranscations()


if __name__ == '__main__':
    main()

