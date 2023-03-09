from flask import Flask, request, render_template, url_for, redirect
from dataModule import calculateStockChangebyDate, calculateMacroChange

app = Flask(__name__, static_url_path='', static_folder='../frontend/flask/static', template_folder='../frontend/flask/template')


@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
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
            calculateStockChangebyDate.processAllStocksChange(startDate, endDate)
            return render_template('index.html', type=type, macroChange=None)
        elif stockPriceOnly == "false":
            calculateStockChangebyDate.processAllStocksChange(startDate, endDate)
            macroChange = calculateMacroChange.process_macro_data(type, startDate, endDate)
            print(macroChange)
            return render_template('index.html', type=type, macroChange=macroChange)
        else:
            return render_template('index.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
