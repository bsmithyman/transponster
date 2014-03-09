from flask import Flask, request, redirect, url_for

import os
import urllib2
import json
import pymongo
import datetime

mutelist = ['127.0.0.1']

def getmongodb ():
    MONGO_URI = os.environ.get('MONGOHQ_URL')
    dbname = MONGO_URI.split('/')[-1]

    db = pymongo.MongoClient(MONGO_URI)[dbname]
    return db

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
