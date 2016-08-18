def getMomentum():
    import numpy as np
    from math import sin,cos,sqrt
    phi = 2*np.pi*np.random.random()
    theta = np.pi*np.random.random()
    mag = 10+15*np.random.random()

    # random pid between pion,proton,kaon
    #masses = [0.1396,0.9383,0.4937]
    #index = np.random.random_integers(0,2)
    #mass = masses[index]
    mass = 0
    
    px = mag*sin(phi)*cos(theta)
    py = mag*sin(phi)*sin(theta)
    pz = mag*cos(theta)

    E = sqrt(px**2+py**2+pz**2+mass**2)
    
    return np.array([px,py,pz,E])
