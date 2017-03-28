##
# File name: main.py
#           - This file contains main classes and functions for the project
#
# This program retrieves stock history date from yahoo finance
#   for the provided stock symbol and data range in month or year.
#   It then plots price and generates prediction using polynomial regression.
#
# How to start the project:
# ==> Service through web browser:
#   1>. On command line, issue:
#       python plt.py
#   2> Open web browser, open page "localhost:5000"
#   Then fill out the forms and push the button next to it
# ==> Service through command line:
#   On command line, issue:
#      python runPgm.py
#   Then follows the instruction on command prompt
##

import requests
import csv
import pandas as pd
import datetime as dt
from datetime import datetime
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import StringIO
from flask import make_response

def printException(e, msg):
    print("Got Exception %s" % (type(e)))
    print(msg)

def validateDate(date):
    try:
        datetime.strptime(date, '%Y%m%d')
    except Exception as e:
        raise ValueError("Incorrect data format, should be YYYYMMDD")
    
class StockPredictor(object):
    """ stock predicter interfaced with webpage """
    def __init__(self, name, srange='10y'):
        # stock url
        self.__stockName = name
        self.__stockRange = srange
        self.__stockUrl = 'http://chartapi.finance.yahoo.com/instrument/1.0/' \
                          +name+'/chartdata;type=quote;range='+srange+'/csv'

        # stock data
        self.dates = None
        self.closep = None
        self.highp = None
        self.lowp = None
        self.openp = None
        self.volumn = None
        self.newDates = None
        self.newClosep = None

        # graph
        self.fig = Figure(figsize=(9.3,7))
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.response = None

        # linear regression
        self.linearMod = linear_model.LinearRegression()

        # Prediction
        self.predictedPrice = 0.0

    def getData(self):
        """ retrieve stock data from yahoo finance website, save it in local vars """
        print("\nGetting data from yahoo finance...")
        try:
            sourceCode  = requests.get(self.__stockUrl)
        except Exception as e:
            printException(e, "Oops, invalid symbol. Start over.")
            return

        stockData = []
        splitSource = sourceCode.text.split('\n') # split to lines

        # extract data
        for line in splitSource:
            splitLine = line.split(',')
            if len(splitLine) == 6:
                if "values" not in line and "labels" not in line:
                    stockData.append(line)

        try:
            self.dates, \
            self.closep, \
            self.highp, \
            self.lowp, \
            self.openp, \
            self.volumn = \
            np.loadtxt(stockData,
                       delimiter = ',',
                       unpack = True,
                       converters = {0: mdates.datestr2num})
        except Exception as e:
            printException(e, "Data retrieval failed. Check your symbol...")

    def prepPlotAndPrediction(self):
        """ Preparation for plot and linear Regression"""
        if not np.any(self.dates):
            self.getData()
        try:
            for label in self.ax1.xaxis.get_ticklabels():
                label.set_rotation(45)
            self.ax1.grid(True)

            self.p = np.polyfit(self.dates, self.closep, 5)  # degree=5
            self.ax1.scatter(self.dates, self.closep, color='b', label='Historical Data', s=3)  # Plotting the intitial data points
            self.ax1.plot_date(self.dates, np.polyval(self.p, self.dates), '-', color='g', label='Polynomial Fit ', linewidth=3)
            self.newDates = np.reshape(self.dates, (len(self.dates), 1))
            self.newClosep = np.reshape(self.closep, (len(self.closep), 1))
            self.linearMod.fit(self.newDates, self.newClosep)
            self.ax1.plot_date(self.dates, self.linearMod.predict(self.newDates),
                               '-', color='r', label='Linear Fit', linewidth=3)

        except Exception as e:
            printException(e, "Prep plot failed. Check your symbol and data range...")


    def calculatePrediction(self, date=None):
        """ Calculate the predicted price """
        if date:
            try:
                date = datetime.strptime(date, '%Y%m%d')
                date = "%s" % (date)
                x = mdates.datestr2num(date)
                ffit = self.p[0] * x ** 5 + self.p[1] * x ** 4 + self.p[2] * x ** 3 + \
                       self.p[3] * x ** 2 + self.p[4] * x + self.p[5]
                self.predictedPrice = ffit
            except Exception as e:
                printException(e, "Prediction calculation failed. Check your date...")
        
    def createPlot(self):
        """ Plot the stock data """
        self.prepPlotAndPrediction()

        # create plot
        self.ax1.set_title("Stock Price/Date Chart")
        self.ax1.set_xlabel("Date")
        self.ax1.set_ylabel("Stock Price")
        self.ax1.legend(loc=4)

        # generate image for web posting
        canvas = FigureCanvas(self.fig)
        output = StringIO.StringIO()
        canvas.print_png(output)
        self.response = make_response(output.getvalue())
        self.response.mimetype = 'image/png'

    def getPrediction(self, date):
        """Return the predicted price for the date"""
        self.prepPlotAndPrediction()
        if date:
            self.calculatePrediction(date)
        else:
            print("Invalid date. Prediction can not be produced!")
        return self.predictedPrice

    def getName(self):
        return self.__stockName

    def getRange(self):
        return self.__stockRange


class StockPredictorCmdln(StockPredictor):
    """ Stock predictor used by command line"""
    def __init__(self,name,srange='10y'):
        super(StockPredictorCmdln, self).__init__(name, srange)
        self.ax1 = plt.subplot2grid((1,1),(0,0))

    def createPlot(self):
        """ Plot the stock data """
        self.prepPlotAndPrediction()

        # create plot
        plt.title("Stock Price/Date Chart")
        plt.xlabel("Date")
        plt.ylabel("Stock Price")
        plt.legend(loc=4)
        plt.subplots_adjust(left=0.09, bottom=0.16, right=0.94, top=0.90, wspace=0.2 )
        plt.show()
