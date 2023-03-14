from flask import Flask, request, render_template, url_for, redirect
from dataModule import calculateStockChangebyDate, calculateMacroChange, wordCloud
import time
from pathlib import Path
import json


app = Flask(__name__, static_url_path='', static_folder='../frontend/flask/static', template_folder='../frontend/flask/template')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/api', methods=['GET', 'POST'])
def api():
    stockPriceOnly = request.args.get('stockPriceOnly')
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    stockSymbol = request.args.get('stockSymbol')
    
    startTimestamp, endTimestamp = calculateStockChangebyDate.getTimeStamps(startDate, endDate)
    wordCloud.getWordCloud(startDate, endDate, stockSymbol)

    url = "http://127.0.0.1:8081/?stockPriceOnly=" + stockPriceOnly + "&startDate=" + startDate + "&endDate=" + endDate 
    + "&stockSymbol" + stockSymbol + "&startTimestamp=" + startTimestamp + "&endTimestamp=" + endTimestamp

    return redirect(url)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        type = request.args.get('type')
        # if 'type' in request.form:
        #     calculateStockChangebyDate.processAllStocksChange(request.form['startDate'], request.form['endDate'])
        #     return redirect(request.path,code=302)
        # # if request.form:
        # #     type = request.form['type']
        # #     startDate = request.form['startDate']
        # #     endDate = request.form['endDate']
        # #     print(type, startDate, endDate)
        
        # # return render_template('index.html')
    else:
        type = request.args.get('type')
        stockPriceOnly = request.args.get('stockPriceOnly')
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')
        
        if stockPriceOnly == "true":  # 只要查 stock change
            percentilesFilePath = Path("./dataset/percentiles/" + str(startDate) + "~" + str(endDate) + ".json")
            if not percentilesFilePath.is_file():  # macro change file does not exist
                print("Not calculated before")
                calculateStockChangebyDate.processAllStocksChange(startDate, endDate)

            macroChange = calculateMacroChange.process_macro_data(startDate, endDate)
            percentilesFile = open(percentilesFilePath)
            percentiles = json.load(percentilesFile)
            startTimestamp, endTimestamp = calculateStockChangebyDate.getTimeStamps(startDate, endDate)

            return render_template('index.html', type=type, macroChange=None, percentiles=percentiles, startTimestamp=startTimestamp, endTimestamp=endTimestamp)
        
        elif stockPriceOnly == "false":  # 要查 stock change 跟 macro change
            percentilesFilePath = Path("./dataset/percentiles/" + str(startDate) + "~" + str(endDate) + ".json")
            print(percentilesFilePath)
            if not percentilesFilePath.is_file():  # macro change file does not exist
                print("Not calculated before")
                calculateStockChangebyDate.processAllStocksChange(startDate, endDate)

            macroChange = calculateMacroChange.process_macro_data(startDate, endDate)
            percentilesFile = open(percentilesFilePath)
            percentiles = json.load(percentilesFile)
            startTimestamp, endTimestamp = calculateStockChangebyDate.getTimeStamps(startDate, endDate)

            return render_template('index.html', type=type, macroChange=macroChange, percentiles=percentiles, startTimestamp=startTimestamp, endTimestamp=endTimestamp)
        
        else:  # 第一次進入網頁
            percentilesFilePath = Path("./dataset/percentiles/" + "2023-01-31" + "~" + "2023-02-01.json")
            if not percentilesFilePath.is_file():  # macro change file does not exist
                print("Not calculated before")
                calculateStockChangebyDate.processAllStocksChange("2023-01-31", "2023-02-01")
            
            percentilesFile = open(percentilesFilePath)
            percentiles = json.load(percentilesFile)
            startTimestamp, endTimestamp = calculateStockChangebyDate.getTimeStamps("2023-01-31", "2023-02-01")

            return render_template('index.html', macroChange=None, percentiles=percentiles, startTimestamp=startTimestamp, endTimestamp=endTimestamp)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
