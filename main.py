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
nPVs = 50
nParticlesPerPV = 15


def main() :

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
  if(False) :
    pltOTtime = plt
    SubParticles = pltOTtime.scatter([x for sublist in reconPVtime for x in sublist], [y for sublist in reconVELOz for y in sublist], color='b')
    ReconstrucPV = pltOTtime.scatter(reconPVmeantime, reconVELOmeanz, color='r', marker='s')
    GeneratedPVs = pltOTtime.scatter(tList, zList, color='g', marker='^')
    pltOTtime.legend([GeneratedPVs, SubParticles, ReconstrucPV], ['Generated PV', 'Reconstructed Particle Origin', 'Reconstructed PV'])
    pltOTtime.xlabel('PV time [ps]')
    pltOTtime.ylabel('Z position [mm]')
    pltOTtime.show()




  ## DO STUDIES
  nWrong_Tonly = nWrong_Zonly = nWrong_TZ = 0
  nWrongRECO_Tonly = nWrongRECO_Zonly = nWrongRECO_TZ = 0

  for pv in range(nPVs) :
    for p in range(nParticlesPerPV) :
      pTime = reconPVtime[pv][p]
      pPos  = reconVELOz[pv][p]

      closestPV_T = min( [abs(PVs[i][0] - pTime) for i in range(nPVs)] )
      #print "truePV T: " + str(abs(PVs[pv][0] - pTime))
      #print closestPV_T
      closestPV_Z = min( [abs(PVs[i][3] - pPos)  for i in range(nPVs)] )
      #print "truePV Z: " + str(abs(PVs[pv][3] - pPos))
      #print closestPV_Z
      closestPV_TZ = min( [ sqrt( (PVs[i][0] - pTime)**2 + (PVs[i][3] - pPos)**2 ) for i in range(nPVs)] )
      #print closestPV_TZ

      closestRECOPV_T = min( [abs(reconPVmeantime[i] - pTime) for i in range(nPVs)] )
      closestRECOPV_Z = min( [abs(reconVELOmeanz[i]  - pPos)  for i in range(nPVs)] )
      closestRECOPV_TZ = min( [ sqrt( (reconPVmeantime[i] - pTime)**2 + (reconVELOmeanz[i] - pPos)**2 ) for i in range(nPVs)] )

      if closestPV_T+0.0001 < abs(PVs[pv][0] - pTime) : nWrong_Tonly += 1
      if closestPV_Z+0.0001 < abs(PVs[pv][3] - pPos ) : nWrong_Zonly += 1
      if closestPV_TZ+0.0001 < sqrt( (PVs[pv][0] - pTime)**2 + (PVs[pv][3] - pPos)**2) : nWrong_TZ += 1
      
      if closestRECOPV_T+0.0001 < abs(reconPVmeantime[pv] - pTime) : nWrongRECO_Tonly += 1
      if closestRECOPV_Z+0.0001 < abs(reconVELOmeanz[pv]  - pPos ) : nWrongRECO_Zonly += 1
      if closestRECOPV_TZ+0.0001 < sqrt( (reconPVmeantime[pv] - pTime)**2 + (reconVELOmeanz[pv] - pPos)**2) : nWrongRECO_TZ += 1

  totalParticles = nPVs * nParticlesPerPV
  print " == "
  print "nWrong_Tonly = " + str(nWrong_Tonly) + " / " + str(totalParticles) + " = " + str(float(nWrong_Tonly) / float(totalParticles) * 100.) + " %"
  print "nWrong_Zonly = " + str(nWrong_Zonly) + " / " + str(totalParticles) + " = " + str(float(nWrong_Zonly) / float(totalParticles) * 100.) + " %"
  print "nWrong_TZ = " + str(nWrong_TZ) + " / " + str(totalParticles) + " = " + str(float(nWrong_TZ) / float(totalParticles) * 100.) + " %"
  print " == "
  print "nWrongRECO_Tonly = " + str(nWrongRECO_Tonly) + " / " + str(totalParticles) + " = " + str(float(nWrongRECO_Tonly) / float(totalParticles) * 100.) + " %"
  print "nWrongRECO_Zonly = " + str(nWrongRECO_Zonly) + " / " + str(totalParticles) + " = " + str(float(nWrongRECO_Zonly) / float(totalParticles) * 100.) + " %"
  print "nWrongRECO_TZ = " + str(nWrongRECO_TZ) + " / " + str(totalParticles) + " = " + str(float(nWrongRECO_TZ) / float(totalParticles) * 100.) + " %"
      
  


  xandylist = [[x for sublist in reconPVtime for x in sublist], [y for sublist in reconVELOz for y in sublist]]
  return [ [xandylist[0][i],xandylist[1][i]] for i in range(totalParticles) ]


main()
