#!/usr/bin/env python

import numpy as np
from common import *

def perturb (model, lat, lng):
    z = np.round(90 - float(lat))
    x = np.round(float(lng) + 180)
    model[z,x] = model[z,x] + 1

def disperse (inarr):

    dims = inarr.shape

    dx = 1.
    dz = 1.
    dt = 1e-1

    left   = np.empty(dims)
    right  = np.empty(dims)
    top    = np.empty(dims)
    bottom = np.empty(dims)

    left[:,0] = inarr[:,-1]
    left[:,1:] = inarr[:,:-1]

    right[:,-1] = inarr[:,0]
    right[:,:-1] = inarr[:,1:]

    top[0,:] = np.mean(inarr[0,:])
    top[1:,:] = inarr[:-1,:]

    bottom[-1,:] = np.mean(inarr[-1,:])
    bottom[:-1,:] = inarr[1:,:]

    inarr[:] = inarr + dt * ((left + right - 2*inarr)/dx**2 + (top + bottom - 2*inarr)/dz**2)

if __name__ == '__main__':

    db = getmongodb()
    mcol = db.model
    ipcol = db.ip

    res = mcol.find_one()
    model = bson2arr(res['model'])

    if ipcol.count() > 0:
        for entry in ipcol.find():
            id = entry['_id']
            if (entry['lat']):
                perturb(model, entry['lat'], entry['lng'])
            ipcol.remove({'_id': id})

    disperse(model)
    res['model'] = arr2bson(model)

    mcol.save(res)
