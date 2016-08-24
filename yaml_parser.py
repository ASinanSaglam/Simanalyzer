from __future__ import division, print_function

import yaml
#import os, argparse
#import numpy, h5py, os, sys, yaml
#import argparse, math, itertools

class YParser:
  def __init__(self, yaml_path):
    self.yaml_dict = self.load_yaml(yaml_path)
    self.pars_dict = self.reduce_dict(self.yaml_dict)

  # Yaml loader functions
  def load_yaml(self, file_path):
    '''
    Open a given yaml file and return a yaml dictionary
    
    args: 
      path to file
  
    returns: 
      yaml dictionary
    '''
    f = open(file_path, 'r')
    f = yaml.load(f)
    return f
  
  def _dict_resolve(self, idict, keys):
    '''
    Dictionary resolver, keys argument has to be a list. 
  
    args: 
      dict
      keys
  
    returns: 
      value of the dict 
    '''
    for key in keys:
      try:
        idict = idict[key]
      except KeyError:
        print("Too many keys to _dict_resolve")
        break
  
    return idict
  #
  def fancy_dict_get(self, idict, keys):
    '''
    Parses the given list of key and returns the value
    Keys can be a string formatted as 'key1/key2/key3/.../keyN'
    
    args:
      dict
      keys
  
    returns:
      value of the keyed dictionary
    '''
    if isinstance(keys,str):
      keys = keys.split("/")
  
    assert len(keys) > 0
  
    keyed_dict = _dict_resolve(idict, keys)
  
    return keyed_dict
  #
  def reduce_dict(self, idict, defkey="default"):
    '''
    Reduces the dictionary so that defaults are distributed
    over every option in every level. 
    
    args:
      dict

    returns:
      reduced dict
    '''
    assert isinstance(idict, dict), "Non-dictionary passed to reduce_dict"
    try:
      defaults = idict.pop(defkey)
    except:
      defaults = None

    for key in idict.iterkeys():
      value = idict[key]
      if defaults and isinstance(value, dict):
        self.merge_dicts(value, defaults)
        value = self.reduce_dict(value, defkey)
      elif isinstance(value, dict):
        value = self.reduce_dict(value, defkey)
      else:
        pass

    return idict

  def merge_dict(self, dict1, dict2):
    '''
    Merges two dictionaries together, first dict will have priority over second dict
    when it comes to overwriting values

    args
      dict1
      dict2

    returns
      merged_dict
    '''
    
