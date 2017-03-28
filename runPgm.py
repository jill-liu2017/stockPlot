##
# File name: main.py
#           - This file is the entry program for starting service on command line
#
# This program retrieves stock history date from yahoo finance
#   for the provided stock symbol and data range in month or year.
#   It then plots price and generates prediction using polynomial regression.
#
# How to start the project:
# ==> Service through command line:
#   On command line, issue:
#      python runPgm.py
#   Then follows the instruction on command prompt
##

from main import *

while True:
    stockName = raw_input(">>Enter a valid stock symbol you would like to investigate or 'q' to quit the program: ")
    if stockName.lower() == 'q':
        break

    print("Enter the range of the plotted data in month or year. ")
    print("For example: '3m' for 3 months, '3y' for 3 years. ")
    stockRange = raw_input(">> Data range: ")
    if stockRange[-1] not in ('m', 'y'):
        print("Invalid range. Start over.")
        continue
    a = StockPredictorCmdln(stockName, stockRange)
    # Plot
    a.createPlot()

    # Price Prediction
    while True:
        predictionDate = raw_input(
            "Enter a date in format of YYYYMMDD to predict the stock price on that date or 'n' to move to next symbol:")
        if predictionDate.lower() == 'n':
            break
        try:
            validateDate(predictionDate)
        except Exception as e:
            printException(e, "Invalid date.  Start over...")
            continue

        print("Predicated (linear regression) stock price for '%s'" % (a.getName())),
        print("based on %s data" % (a.getRange()))
        print(datetime.strptime(predictionDate, '%Y%m%d').strftime("on %b %d, %Y is")),
        print(a.getPrediction(predictionDate))
