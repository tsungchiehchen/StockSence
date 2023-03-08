from flask import Flask, request, render_template, session, redirect

app = Flask(__name__, static_url_path='', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        if 'type' in request.form:
            print(request.form)
            return redirect(request.path,code=302)
        # if request.form:
        #     type = request.form['type']
        #     startDate = request.form['startDate']
        #     endDate = request.form['endDate']
        #     print(type, startDate, endDate)
        
        # return render_template('index.html')
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
