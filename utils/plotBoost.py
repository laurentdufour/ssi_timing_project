
from ROOT import *
from math import sqrt

# E = g m c^2
# p = g m v
# p/E = v/c^2 --> beta = pc / E

mPi = 140.
mK  = 494.
mp  = 940.
mBp = 5279.

clight = 2.99792 * 10**8 * 10**(-9) #m/ns
length = 5.0 #m

minp = 1000.
maxp = 30000.



def cBeta(m,p) :
  return p / sqrt(p**2 + m**2)
def cGamma(m,p) :
  return 1. / sqrt(1 - cBeta(m,p)**2)
def cTime(m,l,p) :
  return l / (cBeta(m,p) * clight)

print "pion: "   + str(cTime(mPi, length, 5000))
print "proton: " + str(cTime(mp, length, 5000))

raw_input("make plots?")

def BetaF(m,p) :
  return "("+str(p)+"/sqrt("+str(p)+"**2+"+str(m)+"**2))"
def GammaF(m,p) :
  return "(1./sqrt(1 - "+BetaF(m,p)+"))"
def TimeF(m,l,p) :
  beta = BetaF(m,p)
  time = str(l)+" / ("+beta+"*"+str(clight)+")"
  return time

betaPion = TF1("betaPion", BetaF(mPi,"x"), minp, maxp)
betaKaon = TF1("betaKaon", BetaF(mK,"x"), minp, maxp)
betaProton = TF1("betaProton", BetaF(mp,"x"), minp, maxp)
betaBplus = TF1("betaBplus", BetaF(mBp,"x"), minp, maxp)

timePion = TF1("timePion", TimeF(mPi,length,"x"), minp, maxp)
timeKaon = TF1("timeKaon", TimeF(mK,length,"x"), minp, maxp)
timeProton = TF1("timeProton", TimeF(mp,length,"x"), minp, maxp)
timeBplus = TF1("timeBplus", TimeF(mBp,length,"x"), minp, maxp)







betaPion.SetLineColor(2)
betaKaon.SetLineColor(4)
betaProton.SetLineColor(6)
betaBplus.SetLineColor(7)

timePion.SetLineColor(2)
timeKaon.SetLineColor(4)
timeProton.SetLineColor(6)
timeBplus.SetLineColor(7)


c1 = TCanvas("c1","c1")
betaPion.SetTitle("")
betaPion.GetXaxis().SetTitle("p [MeV]")
betaPion.GetYaxis().SetTitle("beta")
betaPion.Draw()
betaKaon.Draw("same")
betaProton.Draw("same")
#betaBplus.Draw("same")


leg = TLegend(0.73,0.75-0.3,0.9,0.9-0.3)
leg.AddEntry(betaPion,"pion","l")
leg.AddEntry(betaKaon,"Kaon","l")
leg.AddEntry(betaProton,"proton","l")
#leg.AddEntry(betaBplus,"B+","l")
leg.Draw("same")

c1.SaveAs("plotBetas_betas.pdf")


c2 = TCanvas("c2","c2")
timeProton.SetTitle("")
timeProton.GetXaxis().SetTitle("p [MeV]")
timeProton.GetYaxis().SetTitle("arrival time ("+str(length)+" m) [ns]")
timeProton.Draw()
timeKaon.Draw("same")
timePion.Draw("same")
#timeBplus.Draw("same")
leg.Draw("same")

c2.SaveAs("plotBetas_times.pdf")

'''
c3 = TCanvas("c3","c3")
timeDiffProtonPion = TF1("timeDiffProtonPion","timeProton-timePion",minp,maxp)
timeDiffProtonPion.SetTitle("")
timeDiffProtonPion.GetXaxis().SetTitle("p [MeV]")
timeDiffProtonPion.GetYaxis().SetTitle("proton - pion time diff ("+str(length)+" m) [ns]")
timeDiffProtonPion.Draw()
c3.SaveAs("plotBetas_timePionProtonDiff.pdf")
'''
