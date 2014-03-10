from flask import Flask, request, redirect, url_for

import urllib2
import json
import datetime
from common import *

mutelist = ['127.0.0.1']

db = getmongodb()

app = Flask(__name__)

@app.route('/index')
def index ():
    numentries = db.ip.count()
    return 'Number of entries: %d'%(numentries,)

@app.route('/')
def ip ():
    now = datetime.datetime.utcnow()
    resp = urllib2.urlopen('http://api.hostip.info/get_json.php?ip={}&position=true'.format(request.remote_addr))
    info = json.loads(resp.read())
    info.update({'timestamp': now})

    if not info['ip'] in mutelist:
        db.ip.insert(info)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
