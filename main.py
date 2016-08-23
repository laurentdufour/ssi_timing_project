from makePV import makePV
from math import sqrt
import detector
import propagate
import mom_generator
from matplotlib import pyplot as plt

nTrials = 1

nPVs = 1
nParticlesPerPV = 50


# generate PVs
PVs = [0] * nPVs
for i in range(nPVs) :
  PVs[i] = makePV()

#print PVs

# generate particles
particles = [ [0] * nParticlesPerPV] * nPVs

reconOTtime = [ [0] * nParticlesPerPV] * nPVs
reconVELOz = [ [0] * nParticlesPerPV] * nPVs

for pv in range(nPVs):

    for i in range(nParticlesPerPV) :

        veloZ = detector.get_velo_detector_response(PVs[pv])

        #print [veloZ, PVs[pv][3]]

        [tOT, xOT, yOT, zOT] = propagate.propagate(detector.timing_detector["position_z"],  PVs[pv], mom_generator.getMomentum())
        OTt = detector.get_timing_detector_response([tOT, xOT, yOT, zOT])
        #print OTt

        reconOTtime[pv][i] = OTt
        reconVELOz[pv][i] = veloZ

# plot PVs
'''
zList = []
tList = []
for pv in PVs :
  zList += [pv[3]]
  tList += [pv[0]]
pltPV = plt
pltPV.scatter(zList,tList)
pltPV.xlabel('PV z [mm]')
pltPV.ylabel('PV t [ns]')
pltPV.show()
'''

# plot reconstructed PVs
pltOTtime = plt
print [x for sublist in reconOTtime for x in sublist]

pltOTtime.scatter([x for sublist in reconOTtime for x in sublist], [y for sublist in reconVELOz for y in sublist])
#pltOTtime.scatter(reconOTtime, reconVELOz)
pltOTtime.xlabel('OT times [ns]')
pltOTtime.ylabel('recon Zpos [mm]')
pltOTtime.show()

