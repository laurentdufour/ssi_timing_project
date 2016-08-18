
import numpy as np
from units import mm, mm_to_ps, ps

def makePV(meanx=0.*mm, meany=0.*mm, meanz=0.*mm, meant=0.*mm_to_ps, 
    spreadx=0.*mm, spready=0.*mm, spreadz=50.*mm, spreadt=50.*mm*mm_to_ps, 
    ztcorr = 0.) :

  '''
  creates a PV (= list of [time (ns), x(mm), y(mm), z(mm)] )
  '''

  x = 0; y = 0; z = 0; t = 0;
  if not (meanx==0 and spreadx==0) : x = np.random.normal(meanx, spreadx)
  if not (meany==0 and spready==0) : y = np.random.normal(meany, spready)
  if not (meanz==0 and spreadz==0) : z = np.random.normal(meanz, spreadz)
  if not (meant==0 and spreadt==0) : t = np.random.normal(meant + ztcorr * z, spreadt)

  return [t,x,y,z]

