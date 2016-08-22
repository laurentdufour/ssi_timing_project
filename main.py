
from makePV import makePV

nPVs = 200
nParticlesPerPV = 50


# generate PVs
PVs = {}
for i in range(nPVs) :
  PVs[i] = makePV()

# generate particles
#particles = {}
#  for i in range(nParticlesPerPV) :
    






# plot PVs
zList = []
tList = []
for key,pv in PVs.iteritems() :
  zList += [pv[3]]
  tList += [pv[0]]
from matplotlib import pyplot as pltPV
pltPV.scatter(zList,tList)
pltPV.xlabel('PV z [mm]')
pltPV.ylabel('PV t [ns]')
pltPV.show()



