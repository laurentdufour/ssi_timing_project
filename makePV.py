
import numpy as np

def makePV(meanx=0., meany=0., meanz=0., meanct=0., spreadx=0., spready=0., spreadz=50., spreadct=50., zctcorr = 0.) :
  x = 0; y = 0; z = 0; ct = 0;
  if not (meanx==0  and spreadx==0)  : x = np.random.normal(meanx, spreadx)
  if not (meany==0  and spready==0)  : y = np.random.normal(meany, spready)
  if not (meanz==0  and spreadz==0)  : z = np.random.normal(meanz, spreadz)
  if not (meanct==0 and spreadct==0) : ct = np.random.normal(meanct + zctcorr * z, spreadct)

  return [ct,x,y,z]

