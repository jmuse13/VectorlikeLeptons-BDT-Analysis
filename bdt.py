from helpers import *
from bdt_helpers import *
import sys
import os
import ROOT
import argparse
from root_numpy import array2root
from train_config import *
import pickle

ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser()
parser.add_argument("--i",type=str,default="null",help="Input directory")
parser.add_argument("--o",type=str,default="out",help="Output directory")
parser.add_argument("--a",type=str,default="null",help="Apply BDT directory")
parser.add_argument("--apply",type=int,default=0,help="Apply BDT?")
parser.add_argument("--trainit",type=int,default=0,help="Train BDT?")
parser.add_argument("--r",type=str,default="null",help="Lepton final state")
parser.add_argument("--c",type=float,default=0,help="MET cut")
parser.add_argument("--optimize",type=int,default=0,help="Optimize hyper-parameters")
parser.add_argument("--applyregion",type=str,default='null',help="Final state to apply BDT")
parser.add_argument("--dosys",type=int,default=0,help="Do systematics")
parser.add_argument("--optimize_variables",type=int,default=0,help="Optimize variables")
parser.add_argument("--njobs",type=int,default=1,help="Number of parallel jobs")
args = parser.parse_args()

inPath = args.i
appPath = args.a

print('#############################')
print('#############################')
print('#############################')
print('Looking at: '+inPath)
print('Output will be written to: '+args.o)
print('Regions: '+args.r)
print('Apply to: '+args.applyregion)

inBkg = ['fakes','multiboson','rare_top','ttbar','tth','ttw','ttz','W_jets','WW','WZ','Z_jets','ZZ']
inSig = ['mtaup800','mtaup900','mtaup1000']
print('Backgrounds: '+str(inBkg))
print('Signal: '+str(inSig))

inappBkg = ['data','ttt','ttz','W_jets','ZZ','tttt','WW','fakes','multiboson','ttbar','ttw','twz','WZ','single_top','tth','ttww','tz','Z_jets']
inappSig = ['mtaup130','mtaup200','mtaup300','mtaup400','mtaup500','mtaup600','mtaup700','mtaup800','mtaup900','mtaup1000','mtaup1100','mtaup1200','mtaup1300']

inVariables = []
outvariables = []

if(args.optimize == 1 or args.optimize_variables == 1):
    for var in regionNomVariables[args.r]:
        inVariables.append(var)
if(args.optimize == 0 and args.optimize_variables == 0):
    for var in regionVariables[args.r]:
	inVariables.append(var)
    for var in regionNomVariables[args.r]:
	outvariables.append(var)

countvariables = len(inVariables)

outvariables.append('weight')

print('Variables: '+str(inVariables))
print('#############################')
print('#############################')
print('#############################')

os.system('mkdir '+args.o+'/'+args.applyregion)
outpath = args.o+'/'+args.applyregion+'/'

print('Making dataframe for: '+args.r)

cut = 0
weight_cut = 0

metcut = "filtered(MET,"+str(cut)+")"
weightcut = "filtered(weight,"+str(weight_cut)+")"

ROOT.gInterpreter.Declare("""
bool filtered(float variable,float cut) {
    return variable >= cut;
}
""")

if(args.optimize_variables==1):
    optimize_variables(inPath,inSig,inBkg,inVariables,args.r,args.c,args.njobs,args.o)
    sys.exit()
if(args.optimize == 1):
    cut = args.c
    taucut = args.t
    bkgtrainChain = getChain(inPath,args.r,inBkg)
    sigtrainChain = getChain(inPath,args.r,inSig)
    bkgtrainFrame = ROOT.RDataFrame(bkgtrainChain)
    bkgtrainFrame = bkgtrainFrame.Filter("NJet > 0 && weight > 0 && MET >= "+str(cut) + " && pT_leadingTau >= "+str(taucut))
    sigtrainFrame = ROOT.RDataFrame(sigtrainChain)
    sigtrainFrame = sigtrainFrame.Filter("NJet > 0 && pre_weight > 0 && MET >= "+str(cut) + " && pT_leadingTau >= "+str(taucut))
    sigNumpy = makeNumpy(sigtrainFrame,inVariables,'pre_weight')
    bkgNumpy = makeNumpy(bkgtrainFrame,inVariables,'weight')
    bdt,data_dev,data_eval,category_dev,category_eval = optimize_hyper(sigNumpy,bkgNumpy,inVariables,args.optimize,outpath,args.njobs)
    sys.exit()
if(args.trainit == 1):
    for i in range(5):
	j = i+1
        cut = args.c
        bkgtrainChain = getChain(inPath,args.r,inBkg)
        sigtrainChain = getChain(inPath,args.r,inSig)
        bkgtrainFrame = ROOT.RDataFrame(bkgtrainChain)
        bkgtrainFrame = bkgtrainFrame.Filter("NJet > 0 && weight > 0 && MET >= "+str(cut) +" && FOLD != " +str(j))
        sigtrainFrame = ROOT.RDataFrame(sigtrainChain)
        sigtrainFrame = sigtrainFrame.Filter("NJet > 0 && pre_weight > 0 && MET >= "+str(cut) +" && FOLD != " +str(j))
        sigNumpy = makeNumpy(sigtrainFrame,inVariables,'pre_weight')
        bkgNumpy = makeNumpy(bkgtrainFrame,inVariables,'weight')
        bkgtestChain = getChain(inPath,args.r,inBkg)
        sigtestChain = getChain(inPath,args.r,inSig)
        bkgtestFrame = ROOT.RDataFrame(bkgtestChain)
        bkgtestFrame = bkgtestFrame.Filter("NJet > 0 && weight > 0 && MET >= "+str(cut) +" && FOLD == " +str(j))
        sigtestFrame = ROOT.RDataFrame(sigtestChain)
        sigtestFrame = sigtestFrame.Filter("NJet > 0 && pre_weight > 0 && MET >= "+str(cut) +" && FOLD == " +str(j))
        sigtestNumpy = makeNumpy(sigtestFrame,inVariables,'pre_weight')
        bkgtestNumpy = makeNumpy(bkgtestFrame,inVariables,'weight')
        print('Training BDT, fold: ',str(i))
        bdt = train(sigNumpy,bkgNumpy,sigtestNumpy,bkgtestNumpy,inVariables,args.optimize,outpath,args.r,j)
	picklefilename = "models/"+args.r+"_"+str(i)+".sav"
	pickle.dump(bdt,open(picklefilename,'wb'))
if(args.apply == 1):
    for i in range(5):
        j = i+1
        cut = args.c
        picklefilename = "models/"+args.r+"_"+str(i)+".sav"
	bdt = pickle.load(open(picklefilename,'rb'))
        for sig in inappSig:
            outFile = ROOT.TFile(outpath+sig+'_'+str(j)+'.root','RECREATE')
            outFile.Close()
        for bkg in inappBkg:
            outFile = ROOT.TFile(outpath+bkg+'_'+str(j)+'.root','RECREATE')
            outFile.Close()
        for sig in inappSig:
            print('Making output for '+sig)
            inFile = ROOT.TFile(appPath+'/'+args.applyregion+'/'+sig+'.root')
            if(args.dosys == 1):
                for key in inFile.GetListOfKeys():
                    thisObj = key.ReadObj()
                    if(thisObj.ClassName() == 'TTree'):
    			if(thisObj.GetName() == 'NOSYS'):
                            sysname = thisObj.GetName()
                            print("Doing sys: " + sysname)
			    tempInVariables = []
			    for variable in outvariables:
		                tempInVariables.append(variable)
			    nosystree = inFile.Get('NOSYS')
	                    for b in nosystree.GetListOfBranches():
				if(b.GetName() != 'weight'):
				    splitbranch = b.GetName().split("_")
				    if(splitbranch[0] == 'weight'):
					tempInVariables.append(b.GetName())
		            print("new variables with weight systematics:")
		 	    print(tempInVariables)
                            tempFrame = ROOT.RDataFrame(sysname,appPath+'/'+args.applyregion+'/'+sig+'.root')
                            tempappFrame = tempFrame.Filter("MET > -1 && FOLD == " +str(j))
                            tempNumpy = makeNumpy(tempappFrame,inVariables,'weight')
                            outtempFrame = ROOT.RDataFrame(sysname,appPath+'/'+args.applyregion+'/'+sig+'.root')
                            outtempappFrame = outtempFrame.Filter("MET > -1 && FOLD == " +str(j))
                            outtempNumpy = makeNumpy(outtempappFrame,tempInVariables,'weight')
			    apply_2_tree(tempNumpy,bdt,outpath,sig,inVariables,sysname,1,countvariables,tempInVariables,outtempNumpy,j)
                        if(thisObj.GetName() != 'NOSYS'):
                            sysname = thisObj.GetName()
                            print("Doing sys: " + sysname)
                            tempFrame = ROOT.RDataFrame(sysname,appPath+'/'+args.applyregion+'/'+sig+'.root')
                            tempappFrame = tempFrame.Filter("MET > -1 && FOLD == " +str(j))
                            tempNumpy = makeNumpy(tempappFrame,inVariables,'weight')
                            outtempFrame = ROOT.RDataFrame(sysname,appPath+'/'+args.applyregion+'/'+sig+'.root')
                            outtempappFrame = outtempFrame.Filter("MET > -1 && FOLD == " +str(j))
                            outtempNumpy = makeNumpy(outtempappFrame,outvariables,'weight')
                            apply_2_tree(tempNumpy,bdt,outpath,sig,inVariables,sysname,1,countvariables,outvariables,outtempNumpy,j)
            if(args.dosys == 0):
                if(inFile.GetListOfKeys().Contains('NOSYS')):
                    tempFrame = ROOT.RDataFrame('NOSYS',appPath+'/'+args.applyregion+'/'+sig+'.root')
                    tempappFrame = tempFrame.Filter("MET > -1 && FOLD == " +str(j))
                    tempNumpy = makeNumpy(tempappFrame,inVariables,'weight')
                    outtempFrame = ROOT.RDataFrame('NOSYS',appPath+'/'+args.applyregion+'/'+sig+'.root')
                    outtempappFrame = outtempFrame.Filter("MET > -1 && FOLD == " +str(j))
                    outtempNumpy = makeNumpy(outtempappFrame,outvariables,'weight')
		    apply_2_tree(tempNumpy,bdt,outpath,sig,inVariables,'NOSYS',0,countvariables,outvariables,outtempNumpy,j)
        for bkg in inappBkg:
	    print('Making output for '+bkg)
	    inFile = ROOT.TFile(appPath+'/'+args.applyregion+'/'+bkg+'.root')
            if(args.dosys == 1):
	        for key in inFile.GetListOfKeys():
		    thisObj = key.ReadObj()
                    if(thisObj.ClassName() == 'TTree'):
                        if(thisObj.GetName() == 'NOSYS'):
		            sysname = thisObj.GetName()
                            print("Doing sys: " + sysname)
			    tempInVariables = []
                            for variable in outvariables:
                                tempInVariables.append(variable)
                            nosystree = inFile.Get('NOSYS')
                            for b in nosystree.GetListOfBranches():
                                if(b.GetName() != 'weight'):
                                    splitbranch = b.GetName().split("_")
                                    if(splitbranch[0] == 'weight'):
                                        tempInVariables.append(b.GetName())
                            print("new variables with weight systematics:")
                            print(tempInVariables)
			    tempFrame = ROOT.RDataFrame(sysname,appPath+'/'+args.applyregion+'/'+bkg+'.root')
                	    tempappFrame = tempFrame.Filter("MET > -1 && FOLD == " +str(j))
              		    tempNumpy = makeNumpy(tempappFrame,inVariables,'weight') 
                            outtempFrame = ROOT.RDataFrame(sysname,appPath+'/'+args.applyregion+'/'+bkg+'.root')
                            outtempappFrame = outtempFrame.Filter("MET > -1 && FOLD == " +str(j))
                            outtempNumpy = makeNumpy(outtempappFrame,tempInVariables,'weight')
                            apply_2_tree(tempNumpy,bdt,outpath,bkg,inVariables,sysname,1,countvariables,tempInVariables,outtempNumpy,j)
		        if(thisObj.GetName() != 'NOSYS'):
                            sysname = thisObj.GetName()
                            print("Doing sys: " + sysname)
                            tempFrame = ROOT.RDataFrame(sysname,appPath+'/'+args.applyregion+'/'+bkg+'.root')
                            tempappFrame = tempFrame.Filter("MET > -1 && FOLD == " +str(j))
                            tempNumpy = makeNumpy(tempappFrame,inVariables,'weight')
                            outtempFrame = ROOT.RDataFrame(sysname,appPath+'/'+args.applyregion+'/'+bkg+'.root')
                            outtempappFrame = outtempFrame.Filter("MET > -1 && FOLD == " +str(j))
                            outtempNumpy = makeNumpy(outtempappFrame,outvariables,'weight')
                            apply_2_tree(tempNumpy,bdt,outpath,bkg,inVariables,sysname,1,countvariables,outvariables,outtempNumpy,j)
            if(args.dosys == 0):
	       if(inFile.GetListOfKeys().Contains('NOSYS')):
	            tempFrame = ROOT.RDataFrame('NOSYS',appPath+'/'+args.applyregion+'/'+bkg+'.root')
	            tempappFrame = tempFrame.Filter("MET > -1 && FOLD == " +str(j))
	            tempNumpy = makeNumpy(tempappFrame,inVariables,'weight')	
                    outtempFrame = ROOT.RDataFrame('NOSYS',appPath+'/'+args.applyregion+'/'+bkg+'.root')
                    outtempappFrame = outtempFrame.Filter("MET > -1 && FOLD == " +str(j))
                    outtempNumpy = makeNumpy(outtempappFrame,outvariables,'weight')
                    apply_2_tree(tempNumpy,bdt,outpath,bkg,inVariables,'NOSYS',0,countvariables,outvariables,outtempNumpy,j)

