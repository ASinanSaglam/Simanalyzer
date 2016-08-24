from __future__ import division, print_function

import argparse

from yaml_parser import *
from analysis_runner import *
#import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-yaml', dest="yaml", type=str, help='Yaml file containing the simulation info')
args = parser.parse_args()

## The main purpose of this file is to 
## Run the analyses given a yaml file
if __name__ == "__main__":
  # Read in the yaml file
  yaml = load_yaml(args.yaml)
  # Now we want to run the analyses
  AnalyzerInst = Analyzer(yaml)
  AnalyzerInst.run()
  # Print a report
  #AnalyzerInst.print_report()
