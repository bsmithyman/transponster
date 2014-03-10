

def disperse (inarr):
    import numpy as np

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

    outarr = inarr + dt * ((left + right - 2*inarr)/dx**2 + (top + bottom - 2*inarr)/dz**2)

    return outarr
