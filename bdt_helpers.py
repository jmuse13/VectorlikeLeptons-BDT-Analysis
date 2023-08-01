from train_config import *
from helpers import *
import numpy as np
import numpy.lib.recfunctions as rfn
import matplotlib.pylab as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import cross_val_score
from scipy.stats import uniform, randint
from root_numpy import array2tree, array2root
import array
import multiprocessing as mp

def format_data(insig,inbkg,variables):
    sigtemp = np.array(list(insig.items()))
    bkgtemp = np.array(list(inbkg.items()))
    sig_list = []
    bkg_list = []
    sig_weight_list = []
    bkg_weight_list = []
    for i in range(len(variables)):
	sig_list.append(sigtemp[i,1])
	bkg_list.append(bkgtemp[i,1])
        sig = np.stack(sig_list).T
        bkg = np.stack(bkg_list).T
    data = np.concatenate((sig,bkg))
    category = np.concatenate((np.ones(sig.shape[0]),np.zeros(bkg.shape[0])))
    df = pd.DataFrame(np.hstack((data,category.reshape(category.shape[0],-1))),columns=variables+['category'])
    return df,data,category

def format_for_apply(insample,variables):
    temp = np.array(list(insample.items()))
    temp_list = []
    for i in range(len(variables)):
        temp_list.append(temp[i,1])
    tempout = np.stack(temp_list).T
    return tempout

def check_performance(bdt,data_train,data_test,category_train,category_test,region,path,fold):
    test_predicted = bdt.predict(data_test)
    print('Testing performance:')
    print classification_report(category_test, test_predicted,target_names=["background", "signal"])
    print "Area under ROC curve: %.4f"%(roc_auc_score(category_test,bdt.decision_function(data_test)))

    train_predicted = bdt.predict(data_train)
    print('Training performance:')
    print classification_report(category_train, train_predicted,target_names=["background", "signal"])
    print "Area under ROC curve: %.4f"%(roc_auc_score(category_train,bdt.decision_function(data_train)))

def optimize_hyper(insig,inbkg,variables,optimize,path,njobs):
    df,data,category = format_data(insig,inbkg,variables)
    data_dev,data_eval,category_dev,category_eval = train_test_split(data,category,test_size=0.2,random_state=111)

    dt1 = DecisionTreeClassifier(min_samples_leaf=int(0.05*len(data_dev)),max_depth=8,max_features='sqrt',min_samples_split=0.05)
    bdt1 = AdaBoostClassifier(dt1,algorithm='SAMME')
    print bdt1
    params1 = {"n_estimators": range(20,81,10)}
    search1 = GridSearchCV(bdt1,params1, scoring = 'roc_auc',cv=5, verbose=4, n_jobs=njobs)
    out1 = search1.fit(data_dev[:,0:len(variables)-1],category_dev,sample_weight=data_dev[:,len(variables)-1])
    print search1.best_estimator_
    print search1.best_score_

    bdt2 = search1.best_estimator_
    params2 = {"base_estimator__max_depth": range(5,16,2),"base_estimator__min_samples_split": [0.02,0.05,0.2,0.4,0.6,0.8,1.0]}
    search2 = GridSearchCV(bdt2,params2, scoring = 'roc_auc', cv=5, verbose=4, n_jobs=njobs)
    out2 = search2.fit(data_dev[:,0:len(variables)-1],category_dev,sample_weight=data_dev[:,len(variables)-1])
    print search2.best_estimator_
    print search2.best_score_

    bdt3 = search2.best_estimator_
    params3 = {"base_estimator__min_weight_fraction_leaf": [0.05,0.2,0.4,0.5],"base_estimator__min_samples_split": [0.02,0.05,0.2,0.4,0.6,0.8,1.0]}
    search3 = GridSearchCV(bdt3,params3, scoring = 'roc_auc', cv=5, verbose=4, n_jobs=njobs)
    out3 = search3.fit(data_dev[:,0:len(variables)-1],category_dev,sample_weight=data_dev[:,len(variables)-1])
    print search3.best_estimator_
    print search3.best_score_

    bdt4 = search3.best_estimator_
    params4 = {"base_estimator__max_features": [0.05,0.2,0.4,0.6,0.8,1.0]}
    search4 = GridSearchCV(bdt4, params4, scoring = 'roc_auc', cv=5, verbose=4, n_jobs=njobs)
    out4 = search4.fit(data_dev[:,0:len(variables)-1],category_dev,sample_weight=data_dev[:,len(variables)-1])
    print search4.best_estimator_
    print search4.best_score_

    bdt5 = search4.best_estimator_
    params5 = {"learning_rate": [0.005,0.2,0.4,0.6,0.8,1.0],"n_estimators": range(10,2010,500)}
    search5 = GridSearchCV(bdt5, params5, scoring = 'roc_auc', cv=5, verbose=4, n_jobs=njobs)
    out5 = search5.fit(data_dev[:,0:len(variables)-1],category_dev,sample_weight=data_dev[:,len(variables)-1])
    bdt6 = search5.best_estimator_

    paramsnom = {"base_estimator__max_depth":[2],"base_estimator__min_samples_leaf":[int(0.05*len(data_dev))],"n_estimators":[400],"learning_rate":[0.5]}
    dtnom = DecisionTreeClassifier()
    bdtnom = AdaBoostClassifier(dtnom,algorithm='SAMME')
    searchnom = GridSearchCV(bdtnom, paramsnom, scoring = 'roc_auc', cv=3, verbose=4, n_jobs=njobs)
    outnom = searchnom.fit(data_dev[:,0:len(variables)-1],category_dev,sample_weight=data_dev[:,len(variables)-1])

    print "Best parameter set found on development set:"
    print
    print search5.best_estimator_
    print search5.best_score_
    print "Nominal settings on development set:"
    print
    print searchnom.best_estimator_
    print searchnom.best_score_
    return search5.best_estimator_,data_dev,data_eval,category_dev,category_eval

def optimize_variables(inPath,insig,inbkg,variables,region,cut,njobs,outpath):
    dev_auc_scores = []
    ev_auc_scores = []
    auc_scores = []
    temp_variables = variables
    num_variables = []
    for i in range(len(variables)-1):
        maxval = 1000000
        maxint = 100
        bkgtrainChain = getChain(inPath,region,inbkg)
        sigtrainChain = getChain(inPath,region,insig)
        bkgtrainFrame = ROOT.RDataFrame(bkgtrainChain)
        bkgtrainFrame = bkgtrainFrame.Filter("NJet > 0 && weight > 0 && MET >= "+str(cut))
        sigtrainFrame = ROOT.RDataFrame(sigtrainChain)
        sigtrainFrame = sigtrainFrame.Filter("NJet > 0 && weight > 0 && MET >= "+str(cut))
        sigNumpy = makeNumpy(sigtrainFrame,temp_variables,'pre_weight')
        bkgNumpy = makeNumpy(bkgtrainFrame,temp_variables,'weight')
        df,data,category = format_data(sigNumpy,bkgNumpy,temp_variables)
	data_dev,data_eval,category_dev,category_eval = train_test_split(data,category,test_size=0.2,random_state=111)
        dt = DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=max_depth[region],
        max_features=max_features[region], max_leaf_nodes=None,
        min_impurity_decrease=0.0, min_impurity_split=None,
        min_samples_leaf=int(0.05*len(data_dev)), min_samples_split=min_samples_split[region],
        min_weight_fraction_leaf=min_weight_fraction_leaf[region], presort=False,
        random_state=1, splitter='best')
	bdt = AdaBoostClassifier(dt,algorithm='SAMME',learning_rate=learning_rate[region], n_estimators=n_estimators[region], random_state=1)
	bdt.fit(data_dev[:,0:len(temp_variables)-1],category_dev,sample_weight=data_dev[:,len(temp_variables)-1])
        auc_scores.append(roc_auc_score(category,bdt.decision_function(data[:,0:len(temp_variables)-1])))
        check_overtraining(bdt,data_dev[:,0:len(variables)-1],data_eval[:,0:len(variables)-1],category_dev,category_eval,region,outpath+"/"+region,i)
	num_variables.append(len(temp_variables)-1)
        feat_imp = pd.Series(bdt.feature_importances_).values
	print("Iteration: "+str(i))
        print("Num Vars: "+str(len(temp_variables)-1))
	print("ROC Score: "+str(roc_auc_score(category,bdt.decision_function(data[:,0:len(temp_variables)-1]))))
	print("Variables: ")
        print(temp_variables) 
        for j in range(len(temp_variables)-1):
            if(feat_imp[j] < maxval):
                maxval = feat_imp[j]
                maxint = j
        del temp_variables[maxint]

def getRankings(bdt,variables,path):
    feat_imp = pd.Series(bdt.feature_importances_).values
    return feat_imp

def train(insig,inbkg,intestsig,intestbkg,tvariables,optimize,path,training_region,fold):
    variables = []
    for var in tvariables:
	variables.append(var)
    variables.append('weight') 
    df,data,category = format_data(insig,inbkg,variables)
    dftest,datatest,categorytest = format_data(intestsig,intestbkg,variables)
    dt = DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=max_depth[training_region],
            max_features=max_features[training_region], max_leaf_nodes=None,
            min_impurity_decrease=0.0, min_impurity_split=None,
            min_samples_leaf=int(0.05*len(data)), min_samples_split=min_samples_split[training_region],
            min_weight_fraction_leaf=min_weight_fraction_leaf[training_region], presort=False,
            random_state=1, splitter='best')
    bdt = AdaBoostClassifier(dt,algorithm='SAMME',learning_rate=learning_rate[training_region], n_estimators=n_estimators[training_region], random_state=1)
    print(bdt) 
    bdt.fit(data[:,0:len(variables)-1],category,sample_weight=data[:,len(variables)-1])
    feat_imp = getRankings(bdt,variables,path)
    return bdt

def apply_2_tree(tempNumpy,bdt,outpath,region,tvariables,sysname,doingsys,numvariables,outvariables,outtempNumpy,fold):
    outstring = outpath+'/'+region+'_'+str(fold)+'.root'
    variables = []
    for var in tvariables:
        variables.append(var)
    variables.append('weight')
    data = format_for_apply(tempNumpy,variables)
    outdata = format_for_apply(outtempNumpy,outvariables)
    if(data.shape[0] != 0):
        predicted = bdt.decision_function(data[:,0:numvariables])
	dtp = np.dtype([('bdt_score',np.float64)])
	predictedasarray = np.asarray(predicted,dtp)
        havetree = 0
	outfile = ROOT.TFile(outstring,"READ")
        for key in outfile.GetListOfKeys():
            classname = key.GetClassName()
	    thisObj = ROOT.gROOT.GetClass(classname)
            if(thisObj.InheritsFrom(ROOT.TTree.Class())):
                if(key.GetName() == sysname):
		    havetree = 1
	outfile.Close()
        if(havetree == 0):
	    tree = array2tree(predictedasarray.T)
	    for i in range(len(outvariables)):
                outvar = outvariables[i]
		if(outvariables[i] == "weight_GEN_muR020000E+01_muF010000E+01"):
                    outvar = "weight_GEN_muR020000E_01_muF010000E_01"
		if(outvariables[i] == "weight_GEN_muR050000E+00_muF010000E+01"):
                    outvar = "weight_GEN_muR050000E_00_muF010000E_01"
		if(outvariables[i] == "weight_GEN_muR050000E+00_muF050000E+00"):
                    outvar = "weight_GEN_muR050000E_00_muF050000E_00"
		if(outvariables[i] == "weight_GEN_muR020000E+01_muF020000E+01"):
                    outvar = "weight_GEN_muR020000E_01_muF020000E_01"
		if(outvariables[i] == "weight_GEN_muR010000E+01_muF020000E+01"):
                    outvar = "weight_GEN_muR010000E_01_muF020000E_01"
		if(outvariables[i] == "weight_GEN_muR010000E+01_muF010000E+01"):
                    outvar = "weight_GEN_muR010000E_01_muF010000E_01"
		if(outvariables[i] == "weight_GEN_muR010000E+01_muF050000E+00"):
                    outvar = "weight_GEN_muR010000E_01_muF050000E_00"
		dt = np.dtype([(outvar,np.float64)]) 
	        newarray = np.asarray(outdata[:,i],dt)
	        array2tree(newarray.T,tree=tree)
            outfile = ROOT.TFile(outstring,"UPDATE")
	    tree.SetName(sysname)
            tree.Write()
	    outfile.Close()
        if(havetree != 0):
            outfile = ROOT.TFile(outstring,"UPDATE")
	    treepre = outfile.Get(sysname)
	    tree = treepre.CloneTree()	
	    tree.SetDirectory(0)
            tree2 = array2tree(predictedasarray.T)
            for i in range(len(outvariables)):
                outvar = outvariables[i]
                if(outvariables[i] == "weight_GEN_muR020000E+01_muF010000E+01"):
                    outvar = "weight_GEN_muR020000E_01_muF010000E_01"
                if(outvariables[i] == "weight_GEN_muR050000E+00_muF010000E+01"):
                    outvar = "weight_GEN_muR050000E_00_muF010000E_01"
                if(outvariables[i] == "weight_GEN_muR050000E+00_muF050000E+00"):
                    outvar = "weight_GEN_muR050000E_00_muF050000E_00"
                if(outvariables[i] == "weight_GEN_muR020000E+01_muF020000E+01"):
                    outvar = "weight_GEN_muR020000E_01_muF020000E_01"
                if(outvariables[i] == "weight_GEN_muR010000E+01_muF020000E+01"):
                    outvar = "weight_GEN_muR010000E_01_muF020000E_01"
                if(outvariables[i] == "weight_GEN_muR010000E+01_muF010000E+01"):
                    outvar = "weight_GEN_muR010000E_01_muF010000E_01"
                if(outvariables[i] == "weight_GEN_muR010000E+01_muF050000E+00"):
                    outvar = "weight_GEN_muR010000E_01_muF050000E_00"
                dt = np.dtype([(outvar,np.float64)])   
                newarray = np.asarray(outdata[:,i],dt)
                array2tree(newarray.T,tree=tree2)
	    tlist = ROOT.TList()
	    tlist.Add(tree)
	    tlist.Add(tree2)
	    tree3 = ROOT.TTree.MergeTrees(tlist)
	    tree3.SetName(sysname)
	    outfile.cd()
	    tree3.Write(sysname,ROOT.TObject.kWriteDelete)
	    outfile.Close()
