#!/bin/bash

#If training the BDT, populate the TRAINDIRECTORY line with the training sample from the VLL flat ntuple code and the TRAINIT line with a 1
TRAINDIRECTORY=""
TRAINIT=0
#If optimizing the BDT or BDT variables, set one of the following two lines to 1 in addition to populating the previous lines
OPTIMIZE=0
OPTIMIZEVARIABLES=0

#If applying the BDT, populate the APPLYDIR line with the nominal sample from the VLL flat ntuple code and APPLY with a 1. If doing systematics, change DOSYS to 1
APPLYDIR=""
APPLY=1
DOSYS=0

OUTPUTDIR=out_`date +%F-%s`
NJOBS=1

declare -a regions=("Four_emu" "Two_emuSSOF_One_ta" "Two_emu_Two_ta" "Two_emuOSSF_One_ta" "Three_emu_One_ta" "Three_emu_One_ta" "Two_emuOSOF_One_ta" "Two_emuSSSF_One_ta")
declare -a applyregions=("Four_emu" "Two_emuSSOF_One_ta" "Two_emu_Two_ta" "Two_emuOSSF_One_ta" "Three_emu_Zero_ta" "Three_emu_One_ta" "Two_emuOSOF_One_ta" "Two_emuSSSF_One_ta")
declare -a cuts=(60000 90000 60000 60000 90000 90000 100000 120000)

length=${#applyregions[@]}

mkdir $OUTPUTDIR
for ((i=0;i<${length};i++)); do
    python make_condor_jobs.py --i $TRAINDIRECTORY --o $OUTPUTDIR --a $APPLYDIR --optimize_variables $OPTIMIZEVARIABLES --njobs $NJOBS --trainit $TRAINIT --apply $APPLY --r ${regions[$i]} --c ${cuts[$i]} --optimize $OPTIMIZE --applyregion ${applyregions[$i]} --s $DOSYS --iterator $i --bindirectory $PWD
done
