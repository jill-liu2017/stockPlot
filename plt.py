##
# File name: plt.py
#           - This file is the entry program for starting service in web browser
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
##


from main import *
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def handle_data():
    return render_template('form.html')

@app.route('/result1',methods = ['POST', 'GET'])
def result1():
    if request.method == 'POST':
        stockName = request.form['stockName']
        stockRange = request.form['stockRange']
        if stockRange[-1] not in ('m', 'y'):
            return "Invalid range. Start over."

        # Plot
        plotObj = StockPredictor(stockName, stockRange)
        plotObj.createPlot()
        plotImage = plotObj.response

        return plotImage

@app.route('/result2',methods = ['POST', 'GET'])
def result2():
    if request.method == 'POST':
        stockName = request.form['stockName']
        stockRange = request.form['stockRange']
        if stockRange[-1] not in ('m', 'y'):
            return "Invalid range. Start over."

        predictDate = request.form['predictDate']

        # Plot
        plotObj = StockPredictor(stockName, stockRange)
        plotObj.createPlot()
        plotImage = plotObj.response

        # Price Prediction
        try:
            validateDate(predictDate)
        except Exception as e:
            return "Invalid date. Start over..."
        predictValue = plotObj.getPrediction(predictDate)

        predictDate = datetime.strptime(predictDate, '%Y%m%d').strftime("%b %d, %Y is")
        return render_template("form.html",
                               stockName = stockName,
                               predictDate = predictDate,
                               predictValue = predictValue)

if __name__ == '__main__':
   app.run(debug = True)

