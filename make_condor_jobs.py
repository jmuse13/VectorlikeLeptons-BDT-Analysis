import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--i",type=str,default="null",help="Input directory")
parser.add_argument("--o",type=str,default="out",help="Output directory")
parser.add_argument("--a",type=str,default="null",help="Apply directory")
parser.add_argument("--optimize",type=str,default="null",help="Optimize?")
parser.add_argument("--apply",type=str,default="null",help="Apply?")
parser.add_argument("--trainit",type=str,default="null",help="Train?")
parser.add_argument("--s",type=str,default="null",help="Do systematics?")
parser.add_argument("--r",type=str,default="null",help="Region")
parser.add_argument("--applyregion",type=str,default="null",help="Apply region")
parser.add_argument("--c",type=str,default="null",help="Cut")
parser.add_argument("--iterator",type=str,default="null",help="Iteration")
parser.add_argument("--bindirectory",type=str,default="null",help="Bin directory")
parser.add_argument("--optimize_variables",type=str,default=0,help="Optimize variables")
parser.add_argument("--njobs",type=str,default=1,help="Number of parallel jobs")
args = parser.parse_args()

shfile = open(args.o+'/submit_'+args.iterator+'.sh','w')
shfile.write('#!/bin/bash\n')
shfile.write(' \n')
shfile.write('export ALRB_rootVersion=6.20.06-x86_64-centos7-gcc8-opt\n')
shfile.write('export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase\n')
shfile.write('source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh\n')
shfile.write('lsetup root\n')

shfile.write('python '+args.bindirectory+'/bdt.py --i '+args.i+' --o '+args.bindirectory+'/'+args.o+' --a '+args.a+' --trainit '+args.trainit+' --apply '+args.apply+' --r '+args.r+' --c '+args.c+' --optimize '+args.optimize+' --applyregion '+args.applyregion+' --dosys '+args.s+' --optimize_variables '+args.optimize_variables+' --njobs '+args.njobs+'\n')
shfile.close()
os.system('chmod +x '+args.o+'/submit_'+args.iterator+'.sh')

appfile = open(args.o+'/apply_'+args.iterator+'.sub','w')
appfile.write('log = '+args.bindirectory+'/'+args.o+'/'+args.iterator+'.log\n')
appfile.write('executable = '+args.bindirectory+'/'+args.o+'/submit_'+args.iterator+'.sh\n')
appfile.write('output = '+args.bindirectory+'/'+args.o+'/'+args.iterator+'.out\n')
appfile.write('error = '+args.bindirectory+'/'+args.o+'/'+args.iterator+'.err\n')
appfile.write('request_cpus = 1\n')
appfile.write('request_memory = 25GB\n')
#appfile.write('request_memory = 985\n')
appfile.write('notification = NEVER\n')
appfile.write('universe = vanilla\n')
appfile.write('queue\n')
appfile.close()
os.system('chmod +x '+args.o+'/apply_'+args.iterator+'.sub')
os.system('condor_submit '+args.o+'/apply_'+args.iterator+'.sub')