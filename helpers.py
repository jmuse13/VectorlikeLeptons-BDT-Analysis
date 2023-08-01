import ROOT
import numpy
from collections import OrderedDict

def getChain(inPath,region,inFiles):
    chain = ROOT.TChain("NOSYS")
    for infile in inFiles:
	chain.Add(inPath+region+'/'+infile+'.root')
    return chain

def makeNumpy(dataframe,tinVariables,weight):
    inVariables = []
    for var in tinVariables:
        inVariables.append(var)
    inVariables.append(weight)
    arr = dataframe.AsNumpy(inVariables)
    outarray =OrderedDict()
    for i in range(len(inVariables)):
	outarray[inVariables[i]] = arr[inVariables[i]]
    return outarray


