from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from models import Transaction, Store
import pandas
import tempfile
import seaborn as sns
import random
import calendar
import json
import ipdb
@require_http_methods(['GET', 'POST'])
def index(request):
    agent = request.META['HTTP_USER_AGENT'].lower()
    if "android" in agent or "iphone" in agent:
        aspect=1.5
    else:
        aspect=2

    return render(request, 'index.html', {"lineChart": createLineChart(aspect), "scatterPlot": createScatterplot(aspect), "aspect": aspect})


def createLineChart(aspect):
    """
        Create the actual line chart
        
        :param aspect: The returned graph size. For computers, 2 is recommended.  \
        For mobile phones, 1.5 is the correct size.
        :type aspect: float

        :return: SVG which contains the chart
        :rtype: str
    """
    # Get chart data
    df, states = getLineChartData()
    
    sns.set_style("darkgrid")
    
    fp = sns.factorplot(x='month', y='amount', hue="state", data=df, legend=True, legend_out=False, aspect=aspect)
    fp.set_xlabels('Month')
    fp.set_ylabels('Amount ($)')
    fp.set_xticklabels([calendar.month_abbr[i] for i in xrange(1, 13)])
    fp.ax.legend_.set_title("States")
    # fp.ax.set_title("Sales for 2015")
    svg = getSVG(fp)
    
    return svg

def getLineChartData(numOfTransactions=500):
    """
        Generate random data for the line chart. The data is for two random states

        :param numOfTransactions: The number of random transaction to plot
        :type numOfTransactions: int

        :return: A tuple which contains the dataframe for the chart and a list with the two chosen states
        :rtype: tuple
    """
    
    if numOfTransactions < 1:
        raise ValueError("numOfTransactions must be greater than 0")
    # Choose random two states
    allStates = ['NY', 'NJ', 'CT', 'PA', 'MA']

    statesCheck = set()
    while len(statesCheck) < 3:
        states = [allStates[random.randint(0, 4)] for i in xrange(3)]
        statesCheck = set(states)

    # Filter transcations for only two random states states
    twoStatesTransactions = Transaction.objects.filter(Q(store__state=states[0]) | Q(store__state=states[1]) | Q(store__state=states[2]))
    
    # Create dataframe
    df = pandas.DataFrame(columns=['month', 'amount', 'state'])


 
    for i in xrange(numOfTransactions):
 
        t = random.choice(twoStatesTransactions)

        data = {'month': int(t.date.month), 
                'amount': round(float(t.amount), 2), 
                'state': t.store.state}

        res = df[(df['month']==data['month']) & (df['state']==data['state'])]

        # No transaction for this combination of state and month
        if len(res) == 0:
            df = df.append(pandas.Series(data), ignore_index=True)

        # Add transaction amount to the correct store in the correct month
        else:
            df.set_value(res.index, 'amount', res['amount'] + data['amount'])

    return  (df, states)

def createScatterplot(aspect):
    """
        Create the actual scatter plot
        
        :param aspect: The returned graph size. For computers, 2 is recommended.  \
        For mobile phones, 1.5 is the correct size.
        :type aspect: float
        
        :return: SVG which contains the plot
        :rtype: str
    """
    df, palette = getScatterplotData()
    
    lm = sns.lmplot(x="size", 
                    y="expenses", 
                    hue='ids', 
                    data=df, 
                    legend_out=False, 
                    scatter=True, 
                    fit_reg=False, 
                    palette=palette, 
                    aspect=aspect-0.2)
    
    for i in xrange(len(df)):
        row = df.iloc[i]
        colorIndex = lm.hue_names.index(row['ids'])

        lm.ax.plot(int(row['size']), 
                   float(row['expenses']), 
                   marker='o', 
                   color=palette.as_hex()[colorIndex], 
                   markersize=row.numOfEmployees**0.5)

    # Set chart labels
    lm.set_xlabels('Store Size (sq. ft)')
    lm.set_ylabels('Expenses ($)')
    lm.ax.legend_.set_title('Store ID')
    lm.ax.set_xlim(0, lm.ax.get_xlim()[1])
    # lm.ax.set_title("Store Expenses for 2015")
    
    svg = getSVG(lm)
    
    return svg


def getScatterplotData(numOfStores=8):
    """
        Generate random data for the scatter plot. The data is for eight random stores

        :param numOfStores: The number of random stores to plot
        :type numOfStores: int

        :return: A tuple which contains the dataframe for the chart and the color palette of the plot
        :rtype: tuple
    """
    
    if numOfStores < 1:
        raise ValueError("numOfSotres must be greater than 0")
    # Get all stores
    allStores = Store.objects.all()

    # Choose random stores
    randomStoresIndex = [random.randint(0,len(allStores)-1) for x in xrange(numOfStores)]

    # Create color palette
    palette = sns.color_palette("Set1", n_colors=numOfStores)

    # Generate chart data
    stores = [allStores[i] for i in randomStoresIndex]
    ids = [x.id for x in stores]
    location = [x.state for x in stores]
    size = [x.size for x in stores]
    expenses = [round(float(x.expenses), 2) for x in stores]
    emps = [x.numOfEmployees for x in stores]


    df = pandas.DataFrame({'location': location, 
                           'size': size, 
                           'expenses': expenses, 
                           "numOfEmployees": emps, 
                           "ids": ids})

    return (df, palette)

@require_http_methods(['POST'])
def randomizeLineChart(request):
    """
        Create and return a random line chart

        :rtype: dict
    """
    return HttpResponse(json.dumps({"svg": createLineChart(float(request.POST['aspect']))}),
                        content_type='application/json')
    

@require_http_methods(['POST'])    
def randomizeScatterPlot(request):
    """
        Create and return a random scatter plot

        :rtype: dict
    """
    return HttpResponse(json.dumps({"svg": createScatterplot(float(request.POST['aspect']))}),
                        content_type='application/json')


def getSVG(plot):
    """
        Converts a seaborn plot to SVG string

        :param plot: The plot to convert
        :type plot: seaborn.axisgrid.FacetGrid
        :return: A string which contains the SVG content
        :rtype: str
    """
    f = tempfile.TemporaryFile()
    plot.savefig(f, format='svg')
    f.seek(0)
    lines = f.readlines()[4:]
    f.close()
    return ''.join(lines).replace('\n','')