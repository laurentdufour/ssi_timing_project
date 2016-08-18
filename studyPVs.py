
from matplotlib import pyplot as plt

execfile('makePV.py')

nPVs = 200

zList = []
tList = []
for i in range(nPVs) :
  #newpv = makePV(ztcorr = 1.)
  newpv = makePV()
  zList += [newpv[3]]
  tList += [newpv[0]]

plt.scatter(zList,tList)
plt.xlabel('PV z [mm]')
plt.ylabel('PV t [ns]')
plt.show()





