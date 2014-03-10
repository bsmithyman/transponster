#!/usr/bin/env python

import numpy as np
from common import *

dims = (180,360)

db = getmongodb()
mcol = db.model

# Reset model db
mcol.drop()

model = np.zeros(dims)
mbson = arr2bson(model)

chunk = {
    'dims':  dims,
    'model': mbson,
}

mcol.save(chunk)
