from math import sqrt
import numpy as np

from makePV import makePV
from detector import get_timing_detector_response as timeDetector
from detector import get_velo_detector_response as veloDetector
from detector import timing_detector as timingDetector
from propagate import propagate as prop
from mom_generator import getMomentum as momentum

def generate_event(nPVs, nParticlesPerPV):
  """
   Generates event information
  """

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

  return {
   "PVs" : PVs,
   "reconOTtime": reconOTtime,
   "reconPVtime": reconPVtime,
   "reconPVmeantime": reconPVmeantime,
   "reconVELOz": reconVELOz,
   "reconVELOmeanz": reconVELOmeanz,
   "zList": zList,
   "tList": tList}
"""
  PVs = []
  reconOTtime = []
  reconPVtime = []
  reconPVmeantime = []
  reconVELOz = []
  reconVELOmeanz = []
"""