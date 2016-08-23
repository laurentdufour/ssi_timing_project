from matplotlib import pyplot as plt
from math import sqrt
import numpy as np

from makePV import makePV
from detector import get_timing_detector_response as timeDetector
from detector import get_velo_detector_response as veloDetector
from detector import timing_detector as timingDetector
from propagate import propagate as prop
from mom_generator import getMomentum as momentum

nTrials = 1
nPVs = 200
nParticlesPerPV = 50

# generate lists to store particles' information
PVs = []
reconOTtime = []
reconPVtime = []
reconPVmeantime = []
reconVELOz = []
reconVELOmeanz = []

for pv in range(nPVs):

    # generate PVs
    PVs.append( makePV() )

    #add blank list for each PV for the timing and spatial response
    reconOTtime.append( [] )
    reconPVtime.append( [] )
    reconVELOz.append( [] )

    #calculate meantime and mean position of all PVs
    meantime = 0
    #meanz = 0

    for i in range(nParticlesPerPV) :

        #get vertex locator response for determining z position of PV
        veloZ = veloDetector(PVs[pv])

        #propagate the particle to the timing detector and get time response
        [tOT, xOT, yOT, zOT] = prop(timingDetector["position_z"],  PVs[pv], momentum())
        OTt = timeDetector([tOT, xOT, yOT, zOT])

        #save detector response
        reconOTtime[pv].append( OTt )
        reconVELOz[pv].append( veloZ )

        #save the mean zPosition of the vertex
        #meanz += veloZ / nParticlesPerPV

    reconVELOmeanz.append( np.mean( reconVELOz[pv] ) )

    for i in range(nParticlesPerPV) :

        PVtime = reconOTtime[pv][i] - (timingDetector["position_z"] - reconVELOmeanz[pv])

        #calculate back the production time of the vertex
        reconPVtime[pv].append( PVtime )

    reconPVmeantime.append( np.mean( reconPVtime[pv] ) )

# plot PVs
zList = []
tList = []
for pv in PVs :
  zList += [pv[3]]
  tList += [pv[0]]
'''
pltPV = plt
pltPV.scatter(tList,zList)
pltPV.ylabel('PV t [ps]')
pltPV.xlabel('PV z [mm]')
pltPV.show()
'''
# plot reconstructed PVs
pltOTtime = plt
SubParticles = pltOTtime.scatter([x for sublist in reconPVtime for x in sublist], [y for sublist in reconVELOz for y in sublist], color='b')
ReconstrucPV = pltOTtime.scatter(reconPVmeantime, reconVELOmeanz, color='r', marker='s')
GeneratedPVs = pltOTtime.scatter(tList, zList, color='g', marker='^')
pltOTtime.legend([GeneratedPVs, SubParticles, ReconstrucPV], ['Generated PV', 'Reconstructed Particle Origin', 'Reconstructed PV'])
pltOTtime.xlabel('PV time [ps]')
pltOTtime.ylabel('Z position [mm]')
pltOTtime.show()



