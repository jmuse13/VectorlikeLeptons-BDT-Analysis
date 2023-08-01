# VLL BDT Suite

## Dependencies
* ROOT 6.14 or higher
* Python 2.8 or higher

## Running the code
This package comes with an executable `bdt.py`

On the command line, the following arguments can be passed when calling the main `bdt.py` script:
* `--i`, Input directory
* `--o`, Output directory
* `--apply`, Apply trained BDT
* `--trainit`, Train the BDT
* `--r`, Lepton final state
* `--c`, MET cut to impose in MeV
* `--optimize`, Optimize hyper-parameters
* `--applyregion`, Final state to apply BDT
* `--dosys`, Do systematics
* `--optimize_variables`, Optimize variables
* `--njobs`, Number of parallel jobs

Example for applying the trained BDT on a region with systematics:
```
python bdt.py --i in_directory --o out_directory --apply 1 --r "Four_emu" --c 60000 --applyregion "Four_emu" --dosys 1
```

A script called `run_condor.sh` is provided to run over all regions on condor. The variables in the beginning of the script can be adjusted to perform the desired action.

The code dumps and reads trained BDT models from the `models` directory which is populated by default with the nominal trained BDTs used in the analysis. A copy of the nominal training models is provided in `models_nominal` directory.
