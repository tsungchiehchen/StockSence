from flask import Flask, request, render_template, url_for, redirect
from dataModule import calculateStockChangebyDate, calculateMacroChange
import os
import time

app = Flask(__name__, static_url_path='', static_folder='../frontend/flask/static', template_folder='../frontend/flask/template')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        type = request.args.get('type')
        print(type)
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
        if stockPriceOnly == "true":
            percentiles = calculateStockChangebyDate.processAllStocksChange(startDate, endDate)
            return render_template('index.html', type=type, macroChange=None, percentiles=percentiles)
        elif stockPriceOnly == "false":
            percentiles = calculateStockChangebyDate.processAllStocksChange(startDate, endDate)
            macroChange = calculateMacroChange.process_macro_data(startDate, endDate)
            return render_template('index.html', type=type, macroChange=macroChange, percentiles=percentiles)
        else:  # 第一次進入網頁
            percentiles = calculateStockChangebyDate.processAllStocksChange("2023-01-31", "2023-02-01")
            #macroChange = calculateMacroChange.process_macro_data("2023-01-31", "2023-02-01")
            return render_template('index.html', macroChange=None, percentiles=percentiles)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
