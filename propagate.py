def propagate( zEnd, originVertex, momentum ):
	"""
	Propagates a particle (combination of origin_vertex & momentum)
	to a given z position. 

	Returns a 4-vector (t, x, y, z) with the propagated time,
	x y and z positions. The returned vector always has the
	requested z position, of course.
	"""
        from math import sqrt
        #pT = sqrt(momentum[1]*momentum[1] + momentum[2]*momentum[2])
        #p = sqrt(momentum[1]*momentum[1] + momentum[2]*momentum[2] + momentum[3]*momentum[3])
        
        zToTravel = zEnd - originVertex[3]

        from units import *
        from math import pow
        #c_speed = 3*pow(10,-4)*meter/ps
        #c_speed = 1

        #velocity = [c_speed*momentum[i]/p for i in xrange(1,3)]
        #timeSpentTraveling = zToTravel/velocity[2]

        timeSpentTraveling = zToTravel + originVertex[0]# / sqrt(momentum[3]**2)
        
        #xAtEnd = originVertex[1] + velocity[1] * timeSpentTraveling
        #yAtEnd = originVertex[2] + velocity[2] * timeSpentTraveling

        xAtEnd = 0
        yAtEnd = 0

        return [timeSpentTraveling, xAtEnd, yAtEnd, zEnd ]
