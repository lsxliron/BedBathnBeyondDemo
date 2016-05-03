from __future__ import unicode_literals
from django.db import models
import datetime

class Store(models.Model):
    """
    This class represents one store.

    :param state: The store state. Must be one the following: NY, NJ, CT, PA, MA
    :param numOfEmployees: The number of employees in the store
    :param expenses: The yearly expenses of the store
    :param size: The store size
    :type state: str
    :type numOfEmployees: int
    :type expenses: float
    :type size: int
    """
    states = (('NY', 'NY'), ('NJ', 'NJ'), ('CT', 'CT'), ('PA', 'PA'), ('MA' ,'MA'))
    state = models.CharField(max_length=2, choices=states)
    numOfEmployees = models.IntegerField(default=-1)
    expenses = models.FloatField()
    size = models.IntegerField()

    def __str__(self):
        return "Location: {}\nEmployees: {}\nexpenses: {}\nSize: {}".format(self.state, 
                                                                            self.numOfEmployees, 
                                                                            self.expenses, self.size)

class Transaction(models.Model):
    """
    This class represents a transcation that occured in a store
    
    :param date: The transcation date
    :param amount: The transcation amount
    :param store: The store where the transcation took place
    :type date: datetime
    :type amount: float
    :type store: Store
    """
    date = models.DateField()
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    store = models.ForeignKey(Store)

    def __str__(self):
        return "Amount: {}\ndate: {}\nStore ID:{}".format(self.amount, 
                                                   self.date.strftime('%m/%d/%Y'), 
                                                   self.store.id)
