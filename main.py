from makePV import makePV
import detector
import propagate

nTrials = 1

nPVs = 200
nParticlesPerPV = 50


# generate PVs
PVs = [0] * nPVs
for i in range(nPVs) :
  PVs[i] = makePV()

# generate particles
#particles = [] * nParticlesPerPV
#  for i in range(nParticlesPerPV) :
    






# plot PVs
zList = []
tList = []
for pv in PVs :
  zList += [pv[3]]
  tList += [pv[0]]
from matplotlib import pyplot as pltPV
pltPV.scatter(zList,tList)
pltPV.xlabel('PV z [mm]')
pltPV.ylabel('PV t [ns]')
pltPV.show()



