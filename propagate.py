def propagate( zEnd, origin_vertex, momentum ):
	"""
	Propagates a particle (combination of origin_vertex & momentum)
	to a given z position. 

	Returns a 4-vector (t, x, y, z) with the propagated time, 
	x y and z positions. The returned vector always has the 
	requested z position, of course.
	"""

	pT = sqrt(momentum[1]*momentum[1] + momentum[2]*momentum[2])
	
	zToTravel = zEnd - originVertex[3]

	timeSpentTraveling = zToTravel

        xAtEnd = origin_vertex[1] + momentum[1] * timeSpentTraveling
	yAtEnd = origin_vertex[2] + momentum[2] * timeSpentTraveling

	return [ origin_vertex[0] + timeSpentTraveling, xAtEnd, yAtEnd, zEnd ]
