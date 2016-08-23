def propagate( zEnd, originVertex, momentum ):
	"""
	Propagates a particle (combination of origin_vertex & momentum)
	to a given z position. 

	Returns a 4-vector (t, x, y, z) with the propagated time,
	x y and z positions. The returned vector always has the
	requested z position, of course.
	"""
        from math import sqrt
	pT = sqrt(momentum[0]*momentum[0] + momentum[1]*momentum[1])
        p = sqrt(momentum[0]*momentum[0] + momentum[1]*momentum[1] + momentum[2]*momentum[2])
        
	zToTravel = zEnd - originVertex[2]

        from units import *
        from math import pow
        c_speed = 3*pow(10,-4)*meter/ps

        velocity = [c_speed*momentum[i]/p for i in xrange(0,3)]
        timeSpentTraveling = zToTravel/velocity[2]
        
        xAtEnd = originVertex[0] + velocity[0] * timeSpentTraveling
	yAtEnd = originVertex[1] + velocity[1] * timeSpentTraveling

	return [ xAtEnd, yAtEnd, zEnd, timeSpentTraveling ]
