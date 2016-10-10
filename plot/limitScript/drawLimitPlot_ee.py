import ROOT as R
import glob
import PyROOTUtils
import AtlasStyle, AtlasUtil
R.gROOT.SetBatch()
import sys

#tag = "v9_noStat_noSyst_19Jan_oldNorm_ggF"
#tag = "v9_afs_noSyst_unblind_ggF"
#tag = "v9_noStat_noSyst_19Jan_newRhomin_interp3_ggF"
tag = "llvv_high_mass_ee"
mode = "ggF"

#tag = sys.argv[1]
#mode = sys.argv[2]


#The root file has a 7-bin TH1D named 'limit', where each bin is filled with the upper limit values in this order:
#
#    1: Observed
#    2: Median
#    3: +2 sigma
#    4: +1 sigma
#    5: -1 sigma
#    6: -2 sigma
#    7: mu=0 fit status (only meaningful if asimov data is generated within the macro)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Linear interpolation like numpy.interp
def linear_interp(x, xvals, yvals):
    xvals = [float(v) for v in xvals]
    yvals = [float(v) for v in yvals]
    if x <= xvals[0]: return yvals[0]
    if x >= xvals[-1]: return yvals[-1]
    for iX in range(len(xvals)):
        if x < xvals[iX]:
            break
    # Now iX is the index of xvals just bigger than x
    return yvals[iX-1] + (yvals[iX-1]-yvals[iX])/(xvals[iX-1]-xvals[iX]) * (x-xvals[iX-1])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Can be used to load CX or BR from text file
# assumue first column in text file is mH, second is CX/BR
def get_cxs(filename, masses ):
    f_xs = open(filename,'r')
    vals = []
    file_masses = []
    for line in f_xs:
        line = line.strip().split()
        if len(line)<2: print line
        vals .append( float(line[1]) )
        file_masses .append( float(line[0]) )
    cx = [ linear_interp(mH, file_masses, vals) for mH in masses ] 
    return cx
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


results = {}

class LimitAtMh:
    def __init__(self, mh, th1):
        self.mH = mH
        self.obs = th1.GetBinContent(1)
        self.med = th1.GetBinContent(2)
        self.plus2sigma = th1.GetBinContent(3)
        self.plus1sigma = th1.GetBinContent(4)
        self.minus1sigma = th1.GetBinContent(5)
        self.minus2sigma = th1.GetBinContent(6)
        self.status = th1.GetBinContent(7)
        #print self.mH
        #print self.obs
        #print self.med
        #print self.plus2sigma
        #print self.plus1sigma
        #print self.minus1sigma
        #print self.minus2sigma
        #print self.status

for rfname in glob.glob("root-files/"+tag+"/*.root"):
    mH = float( ".".join(rfname.split('/')[-1].split(".")[:-1]) )
    rf = R.TFile(rfname)
    hist = rf.Get("limit")
  #  hist = rf.Get("limit_old")
    limit = LimitAtMh(mH, hist)
    if limit.status:
       # print "Fit status="+limit.status+" for mH="+str(mH)+" - skiiping "
        continue
    results[mH] = limit

masses = sorted(results.keys())
obsvalues= [ results[mH].obs for mH in masses ] 
medians = [ results[mH].med for mH in masses ] 
plus2sigmas = [ results[mH].plus2sigma for mH in masses ] 
plus1sigmas = [ results[mH].plus1sigma for mH in masses ] 
minus2sigmas = [ results[mH].minus2sigma for mH in masses ] 
minus1sigmas = [ results[mH].minus1sigma for mH in masses ] 

fn_br = './CrossSections/BR_ZZ.txt'#'BR_emu.txt'
#fn_br = './CrossSections/XS_ggF_scaled.txt'#'BR_emu.txt'

br = get_cxs(fn_br, masses)

if (mode=="VBF"):
    # Need t add cx for WH and ZH
    cx_VBF = get_cxs("XS_VBF.txt", masses)
    cx_ZH = get_cxs("XS_ZH.txt", masses)
    cx_WH = get_cxs("XS_WH.txt", masses)
    #xs = [cx_VBF[i]+cx_WH[i]+cx_ZH[i] for i in range(len(masses))]
    xs = [cx_VBF[i] for i in range(len(masses))]
else:
    #xs = get_cxs("XS_ggF_scaled.txt", masses)
    #xs = get_cxs("./CrossSections/XS_ggF_scaled.txt", masses)
    xs = get_cxs("./CrossSections/XS_ggF_new.txt", masses)

#for i,mH in enumerate(masses):
    #print mH, br[i], xs[i], cx_VBF[i], cx_ZH[i], cx_WH[i]

#cx_br

lim_obs=[]
lim_med =[]
minus1sig=[]
plus1sig=[]
minus2sig=[]
plus2sig=[]

sm=[]

for i in range(0,len(medians)):
    #lim_med.append(medians[i])
#    lim_obs.append(float(br[i])*float(xs[i])*obsvalues[i]*1000/0.44)
#    lim_med.append(float(br[i])*float(xs[i])*medians[i]*1000/0.44)
#    minus1sig.append(float(br[i])*float(xs[i])*minus1sigmas[i]*1000/0.44)
#    minus2sig.append(float(br[i])*float(xs[i])*minus2sigmas[i]*1000/0.44)
#    plus1sig.append(float(br[i])*float(xs[i])*plus1sigmas[i]*1000/0.44)
#    plus2sig.append(float(br[i])*float(xs[i])*plus2sigmas[i]*1000/0.44)
#    sm.append(float(br[i])*float(xs[i])*1000/0.44)
    lim_obs.append(float(br[i])*float(xs[i])*obsvalues[i])
    lim_med.append(float(br[i])*float(xs[i])*medians[i])
    minus1sig.append(float(br[i])*float(xs[i])*minus1sigmas[i])
    minus2sig.append(float(br[i])*float(xs[i])*minus2sigmas[i])
    plus1sig.append(float(br[i])*float(xs[i])*plus1sigmas[i])
    plus2sig.append(float(br[i])*float(xs[i])*plus2sigmas[i])
    sm.append(float(br[i])*float(xs[i]))



#    lim_obs.append(25*0.01*float(xs[i])*obsvalues[i]*1000/0.44)
#    lim_med.append(25*0.01*float(xs[i])*medians[i]*1000/0.44)
#    minus1sig.append(25*0.01*float(xs[i])*minus1sigmas[i]*1000/0.44)
#    minus2sig.append(25*0.01*float(xs[i])*minus2sigmas[i]*1000/0.44)
#    plus1sig.append(25*0.01*float(xs[i])*plus1sigmas[i]*1000/0.44)
#    plus2sig.append(25*0.01*float(xs[i])*plus2sigmas[i]*1000/0.44)
#    sm.append(float(br[i])*float(xs[i])*1000/0.44)
 
    #print lim_med[i]

#    #lim_med.append(medians[i])
#    lim_med.append(float(br[i])*float(xs[i])*medians[i]*1000*0.04)
#    minus1sig.append(float(br[i])*float(xs[i])*minus1sigmas[i]*1000*0.04)
#    minus2sig.append(float(br[i])*float(xs[i])*minus2sigmas[i]*1000*0.04)
#    plus1sig.append(float(br[i])*float(xs[i])*plus1sigmas[i]*1000*0.04)
#    plus2sig.append(float(br[i])*float(xs[i])*plus2sigmas[i]*1000*0.04)
#    sm.append(float(br[i])*float(xs[i])*1000*0.04)
#    #print lim_med[i]

###  Write out the limit to .tex file
outputtexfile=open("limitNumbers_ee.tex", "w")
title='''
\\begin{table}
\\begin{center}
\\begin{tabular}{c|cccccc}
\\hline
\\hline
Mass points & Exp. Limits [fb] & Exp. $+2\sigma$ & Exp. $+1\sigma$ &  Exp. $-1\sigma$  &  Exp. $-2\sigma$ & Obs. Limits \\\\
\\hline
'''
outputtexfile.write(title)

for i in range(0,len(medians)):
    masspoint=masses[i]
    line="%s GeV  &  %4.2f  & %4.2f  & %4.2f  & %4.2f  & %4.2f   & %4.2f\\\\"%(str(masspoint), lim_med[i], plus2sig[i], plus1sig[i], minus1sig[i], minus2sig[i], lim_obs[i])
#    line="%s GeV  &  %4.2f  & %4.2f  & %4.2f  & %4.2f  & %4.2f   &  \\\\"%(str(masspoint), lim_med[i], plus2sig[i], plus1sig[i], minus1sig[i], minus2sig[i] )
    print line
    outputtexfile.write(line+"\n")

tail='''
\\hline
\\hline
\end{tabular}
\end{center}
\end{table}
'''
outputtexfile.write(tail)

outputtexfile.close()

#gr_med = PyROOTUtils.Graph(masses, medians)

gr_obs= PyROOTUtils.Graph(masses, lim_obs)
gr_obs.SetMarkerStyle(20);
gr_med = PyROOTUtils.Graph(masses, lim_med)
#gr_med.SetMarkerStyle(7)
gr_med.SetLineStyle(R.kDashed)
gr_med.SetLineWidth(2)
#band_1sigma = PyROOTUtils.Band(masses, minus1sigmas, plus1sigmas, fillColor=R.kGreen)
#band_2sigma = PyROOTUtils.Band(masses, minus2sigmas, plus2sigmas, fillColor=R.kYellow)
band_1sigma = PyROOTUtils.Band(masses, minus1sig, plus1sig, fillColor=R.kGreen)
band_2sigma = PyROOTUtils.Band(masses, minus2sig, plus2sig, fillColor=R.kYellow)

# Prepare frame
hframe = R.TH1I("frame", "frame", 1, min(masses), max(masses))
hframe.GetXaxis().SetTitle("m_{H} [GeV]")
#hframe.GetXaxis().SetRangeUser(300,1000)
#hframe.GetYaxis().SetTitle("95% Limit on #sigma/#sigma_{SM}")
if (mode=='VBF'):
  hframe.GetYaxis().SetTitle("95% Limit on #sigma_{VBF} * BR(H #rightarrow ZZ) [fb]")
else:
  hframe.GetYaxis().SetTitle("95% Limit on #sigma_{ggF} #times BR(H #rightarrow ZZ) [fb]")
c = R.TCanvas("c", "c", 600, 600)
c.SetLogy()
hframe.Draw()
hframe.SetMaximum(1000000)
hframe.SetMinimum(2)
band_2sigma.Draw("f")
band_1sigma.Draw("f")
hframe.Draw("axis,same")

# Draw exclusion line
line = R.TLine(min(masses), 1, max(masses), 1)
line.SetLineStyle(R.kDotted)
line.SetLineColor(R.kRed)
#line.Draw()

gr_med.Draw("L")

gr_obs.SetLineColor(R.kBlack)
gr_obs.SetLineWidth(3)
gr_obs.Draw("L")


sm_pred = PyROOTUtils.Graph(masses, sm)
sm_pred.SetLineWidth(2)
sm_pred.SetLineColor(R.kRed)
#sm_pred.Draw("L,same")

# Draw Legend
leg = PyROOTUtils.Legend(0.60, 0.9, textSize=0.037)
leg.AddEntry(gr_obs, "Observed", "l")
leg.AddEntry(gr_med, "Expected Median", "l")
leg.AddEntry(band_1sigma, "Expected #pm1 #sigma", "f")
leg.AddEntry(band_2sigma, "Expected #pm2 #sigma", "f")
#leg.AddEntry(sm_pred, "#sigma_{SM} x BR", "l")
leg.Draw()

# Draw Text
col_l = 0.19
AtlasUtil.AtlasLabel(col_l, 0.85)
#AtlasUtil.DrawLuminosityFbEcmFirst(col_l, 0.78, 20.3, size=0.037, sqrts=8)
#AtlasUtil.DrawLuminosityFb(col_l, 0.78, 5, 13)
AtlasUtil.DrawLuminosityFb(col_l, 0.78, 13.3, 13)  ## in fb
#AtlasUtil.DrawText(col_l, 0.71, "H#rightarrowZZ*#rightarrow4#font[12]{l}", size=0.037)
AtlasUtil.DrawText(col_l, 0.71, "H #rightarrow ZZ #rightarrow ee#nu#nu", size=0.037)
if (mode=='VBF'):
    AtlasUtil.DrawText(col_l, 0.66, "VBF", size=0.037)
else:
    AtlasUtil.DrawText(col_l, 0.66, "ggF", size=0.037)

c.SaveAs("./limitplots/"+tag+"XSEC_NEW_ee.png")
c.SaveAs("./limitplots/"+tag+"XSEC_NEW_ee.eps")
c.SaveAs("./limitplots/"+tag+"XSEC_NEW_ee.pdf")

ofile = R.TFile("graphs_"+tag+".root", "RECREATE")
gr_med.SetName("median")
gr_med.Write()
band_1sigma.SetName("1sigma")
band_1sigma.Write()
band_2sigma.SetName("2sigma")
band_2sigma.Write()
sm_pred.SetName("sm")
sm_pred.Write()
ofile.Close()
