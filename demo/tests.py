from django.test import TestCase
from demo.models import Store, Transaction
from demo.views import getLineChartData, getScatterplotData
import datetime
import ipdb
import random

class BbbTestCase(TestCase):

    def setUp(self):

        # Setup stores
        allStates = ['NY', 'NJ', 'CT', 'PA', 'MA']
        for i in xrange(100):
            Store.objects.create(state=random.choice(allStates),
                                 numOfEmployees=random.randint(10, 100), 
                                 size=random.randint(100, 1000), 
                                 expenses=random.random()*1000)

        # Setup transactions
        stores = Store.objects.all()
        y = 2015
        for i in xrange(1000):
            d = random.randint(1,28)
            m = random.randint(1,12)
            amount = random.random() * 1000
            store = random.choice(stores)
            transactionDate = datetime.date(y, m, d)
            Transaction.objects.create(amount=amount, date=transactionDate, store=store)
            

            
    def test_scatter_plot_data(self):
        data, palette = getScatterplotData(20)
        self.assertEqual(len(data), 20)

        data, palette = getScatterplotData(30)
        self.assertEqual(len(data), 30)

        with self.assertRaises(ValueError):
            data, palette = getScatterplotData(0)
            data, palette = getScatterplotData(-1)



    def test_lineChart_data(self):
        data, states = getLineChartData(20)
        self.assertLess(len(data), 20)
        self.assertEqual(len(states), 3)

        data, palette = getLineChartData(30)
        self.assertLess(len(data), 30)
        self.assertEqual(len(states), 3)
        
        with self.assertRaises(ValueError):
            data, states = getScatterplotData(0)
            data, states = getScatterplotData(-1)

