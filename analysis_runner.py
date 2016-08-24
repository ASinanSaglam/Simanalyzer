from __future__ import division, print_function

import re
import itertools as itt
#import os, argparse
#import numpy, h5py, os, sys, yaml
#import argparse, math, itertools

# Make a class that will handle the analyses
class Analyzer:
  def __init__(self, yaml_dict):
    self.yaml = yaml_dict
    self.find_regs = re.compile('^__.+__$')
    self.find_meta = re.compile('^__meta__$')
    self.find_defs = re.compile('^__all__$')

  def over_checked(self, dict, checker):
    return itt.ifilter(checker, dict.iterkeys())

  def over_checked_false(self, dict, checker):
    return itt.ifilterfalse(checker, dict.iterkeys())

  def get_settings(self, keys):
    return merge_dicts(self.yaml, keys, ...)

  def _run_analysis(self, analysis_dict):
    raise NotImplementedError

  def run(self):
    nondefs = self.over_checked_false
    checker = self.find_regs
   
    for project in nondefs(self.yaml, checker.match):
      print(project)
      pdict = self.yaml[project]
      for sim in nondefs(pdict, checker.match):
        print(sim)
        sdict = pdict[sim]
        for analysis in nondefs(sdict, checker.match):
          print(analysis)
          analysis_setup = self.get_settings([project, sim, analysis])
          print(analysis_setup)
          #self._run_analysis(analysis_setup)

  def print_report(self):
    raise NotImplementedError

# We need funtions
# 1) run 
# 2) print report

# For run we will need many more
# For print report we will need at least generate_report kinda thing
