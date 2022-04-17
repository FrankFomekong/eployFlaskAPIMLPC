from flask import Flask, request
from flask import render_template
from flask import Response
import joblib
import os
import sys
sys.modules['sklearn.externals.joblib'] = joblib


app = Flask(__name__)
endpoint = '/api/fakedetector'



filename = 'pipeline1.sav'
loadedModel = joblib.load(filename)
@app.route(endpoint, methods=["GET", "POST"])
def detector():
    try:
        if request.method =='GET':
            text = request.args.get('text')
            p = loadedModel.predict([text])[0]
            print(p)
            if p==-1:
                print('fake')
                return {'fake':1,'truth':0}
            else:
                print('true')
                return {'fake':0,'truth':1}
        if request.method == 'POST':
            print(request.get_json())
            mail = request.get_json()['text']
            p = loadedModel.predict([mail])[0]
            print(p)
            if p==-1:
                print('fake')
                return {'fake':1,'truth':0}
            else:
                print('true')
                return {'fake':0,'truth':1}
    except:
        return {'fake':0,'truth':0}
    return {'fake':0,'truth':0}

@app.route("/", methods=['GET', 'POST'])
def main_page():
    opts = {}
    if request.method == 'GET':
        return render_template('main_page.html', opts=opts)
    

# if __name__ == '__main__':
    # app.run(port=8081, debug=True, host='localhost')
if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)