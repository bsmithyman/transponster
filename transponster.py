from flask import Flask, request, redirect, url_for, make_response
from werkzeug.contrib.fixers import ProxyFix

import urllib2
import json
import datetime
from common import *
from PIL import Image
from StringIO import StringIO

mutelist = ['127.0.0.1']

db = getmongodb()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/index')
def index ():
    content = '''
    <html>
      <head>
        <title>Transponster</title>
      </head>
      <body>
        <img src="render.png" />
      </body>
    </html>
    '''

    return content

@app.route('/')
def ip ():
    now = datetime.datetime.utcnow()
    resp = urllib2.urlopen('http://api.hostip.info/get_json.php?ip={}&position=true'.format(request.remote_addr))
    info = json.loads(resp.read())
    info.update({'timestamp': now})

    if not info['ip'] in mutelist:
        db.ip.insert(info)
    
    return redirect(url_for('index'))

@app.route('/render.png')
def render ():
    mcon = db.model
    res = mcon.find_one()
    model = bson2arr(res['model'])

    if model.max() > 0:
        model = 255 * model / model.max()

    output = StringIO()
    Image.fromarray(model).convert('RGB').save(output, format='PNG')

    response = make_response(output.getvalue())
    response.mimetype = 'image/png'

    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

