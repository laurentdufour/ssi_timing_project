
from matplotlib import pyplot as plt

execfile('python/makePV.py')

nPVs = 200

zList = []
ctList = []
for i in range(nPVs) :
  #newpv = makePV(zctcorr = 1.)
  newpv = makePV()
  zList += [newpv[3]]
  ctList += [newpv[0]]

plt.scatter(zList,ctList)
plt.xlabel('PV z [mm]')
plt.ylabel('PV ct [mm]')
plt.show()





