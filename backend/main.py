from flask import Flask, request, render_template, url_for, redirect
from dataModule import calculateStockChangebyDate, calculateMacroChange, wordCloud, getNewsSentiment, hierarchicalClustering
import time
from pathlib import Path
import json


app = Flask(__name__, static_url_path='', static_folder='../frontend/flask/static', template_folder='../frontend/flask/template')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/api', methods=['GET', 'POST'])
def api():
    stockPriceOnly = "true"
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    stockSymbol = request.args.get('stockSymbol')
    treeType = request.args.get('cluster')

    startTimestamp, endTimestamp = calculateStockChangebyDate.getTimeStamps(startDate, endDate)
    rate = calculateStockChangebyDate.getStocksChange(stockSymbol, startDate, endDate)
    
    wordCloud.getWordCloud(startDate, endDate, stockSymbol)
    getNewsSentiment.get_news_sentiment(startDate, endDate, stockSymbol)
    hierarchicalClustering.perform_hierarchical_cluster(stockSymbol)
    
    url = "http://127.0.0.1:8081/?stockPriceOnly=" + str(stockPriceOnly) + "&startDate=" + str(startDate) + "&endDate=" + str(endDate) + "&stockSymbol=" + str(stockSymbol) + "&startTimestamp=" + str(startTimestamp) + "&endTimestamp=" + str(endTimestamp) + "&rate=" + str(rate) + "&treeType=" + str(treeType)

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
            percentilesFilePath = Path("./dataset/percentiles/" + "2022-12-01" + "~" + "2023-01-01.json")
            if not percentilesFilePath.is_file():  # macro change file does not exist
                print("Not calculated before")
                calculateStockChangebyDate.processAllStocksChange("2022-12-01", "2023-01-01")
            
            macroChange = calculateMacroChange.process_macro_data("2022-12-01", "2023-01-01")
            percentilesFile = open(percentilesFilePath)
            percentiles = json.load(percentilesFile)
            startTimestamp, endTimestamp = calculateStockChangebyDate.getTimeStamps("2022-12-01", "2023-01-01")

            return render_template('index.html', macroChange=macroChange, percentiles=percentiles, startTimestamp=startTimestamp, endTimestamp=endTimestamp)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
