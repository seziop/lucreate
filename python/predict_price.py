import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import numpy as np    

list_last_point = []

#def set_ticker(ticker, shares):
#    global closing_set
#    start = dt.datetime(2018, 1, 1)
#    
#    end_year = int(dt.datetime.today().strftime('%Y'))
#    end_month = int(dt.datetime.today().strftime('%m'))
#    end_day = int(dt.datetime.today().strftime('%d'))
#    
#    end = dt.datetime(end_year, end_month, end_day)
#    
#    df = web.DataReader(ticker, 'yahoo', start, end)
#    data_set = df[['Close']]
#    closing_set = data_set.values
#    closing_set = [x*shares for x in closing_set]

test = []
total = []
def total_volume(num_stocks):
    global test
    global total
    year = int(dt.datetime.today().strftime('%Y'))
    day = int(dt.datetime.today().strftime('%d'))
    month = int(dt.datetime.today().strftime('%m'))
    start = dt.datetime(2018,1,1)
    end = dt.datetime(year, month, day)
    for k in range(num_stocks):
        a = input("Enter your stock")
        b = int(input("Enter volume of stock"))
        df = web.DataReader(a, 'yahoo', start, end)
        df1 = df[['Close']]
        data = df1.values
        data = [x*b for x in data]
        test.append(data)
    total = [sum(x) for x in zip(*test)]
    total = [float(x) for x in total]
    

def predict_price(days=1):
    global list_last_point
    rate_of_change = []
    
    for k in range(0, len(total)-1):
        rate_of_change.append(np.log(total[k+1]/total[k]))
    
    S0 = float(total[-1])        
    future_prices = [] 
    
    for i in range(1, days+1):
        future_prices.append(float(total[-i]))
    future_prices.reverse()
    
    avg = np.mean(rate_of_change)    
    std_dev = np.std(rate_of_change)
    variance = std_dev ** 2
    drift = avg - (variance/2)
            
    for i in range(days):
        z = np.random.uniform(-.999999999, .99999999)
        S1 = (S0 * np.exp((drift+(std_dev*z))))
        future_prices.append(S1)
        
        if i == days-1:
            list_last_point.append(S1)
            
        S0 = S1    
    return future_prices

def plot_function(days=1):
    plt.figure(1)
    plt.clf()
    for k in range(300):
        plt.plot(predict_price(days))
    
def plot_trend():
    plt.figure(2)
    plt.clf()
    plt.plot([0]*len(list_last_point), list_last_point, "ks")

def plot_histogram():
    plt.figure(3)
    plt.clf()
    plt.hist(list_last_point, 11)
    
def plot_trendline(days=1):
    val = np.mean(list_last_point)
    plt.figure(1)
    plt.plot([days-1, (days*2)-1], [total[-1], val], 'ks-', markersize=12, linewidth=5)
    
#def run_all(ticker, days, shares):
#    set_ticker(ticker, shares)
#    plot_function(days)
#    plot_trend()
#    plot_histogram()
#    plot_trendline(days)
#    plt.figure(1)
#    plt.title("Stock: " + ticker + " over time", fontsize=26)
#    plt.xlabel("Days", fontsize=20)
#    plt.ylabel("Dollars ($)", fontsize=20)