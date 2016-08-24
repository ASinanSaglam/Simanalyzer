from __future__ import division, print_function

import yaml

#import os, argparse
#import numpy, h5py, os, sys, yaml
#import argparse, math, itertools

# Yaml loader function
def load_yaml(file_path):
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
#  
def _dict_resolve(dict, keys):
  '''
  Dictionary resolver, keys has to be a list. 

  args: 
    dict
    keys

  returns: 
    value of the dict 
  '''
  for key in keys:
    dict = dict[key]

  return dict
#
def fancy_dict_get(dict, keys):
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

  keyed_dict = _dict_resolve(dict, keys)

  return keyed_dict
#

#### NOT FUNCTIONAL/DECIDED YET ####
def make_path(dict, keys):
  try:
    curr = dict[keys[0]]
  except:
    dict[keys[0]] = {}
    curr = dict[keys[0]]
  for key in keys[1:]:
    try:
      curr = curr[key]    
    except:
      curr[key] = {}
      curr = curr[key]
  return dict

def resolve_key(dict, keys):
  print("In resolve keys")
  print(keys)
  if len(keys) == 1:
    return dict[keys[0]]
  print(dict.__class__)
  curr = dict[keys[0]]
  for key in keys[1:]:
    curr = curr[key]
  return curr

def move_path(elem, dict, keys):
  print("In move path")
  print(keys)
  if len(keys) == 1:
    dict2[keys[0]] = dict1.pop(keys[0])
    return dict1, dict2

  key = keys[-1]

  curr1 = resolve_key(dict1, keys[:-1])
  curr2 = resolve_key(dict2, keys[:-1])
  
  curr2[key] = curr1.pop(key)
  
  return dict1, dict2
   
def get_defs_and_meta(dict, defs, meta, keys):
  make_path(defs, keys)  
  make_path(meta, keys)  
  
  lkey = keys[-1]

  if lkey == 'all':
    move_path(dict, defs, keys)
  elif lkey == 'meta':
    move_path(dict, meta, keys)
  else:
    pass

def recurs_yaml(node, yaml, defs, meta, keys):
  if len(keys) >= 1:
    if node.__class__ == dict:
      if len(node.keys()) >= 1:
        for child in yaml.keys():
          keys.append(child)
          node, yaml, defs, meta, keys = recurs_yaml(yaml[child], yaml, defs, meta, keys)
        return node, yaml, defs, meta, keys
      else:
        lkey = keys[-1]
        if lkey == 'all': 
          yaml, defs = move_path(yaml, defs, keys)
          node, yaml, defs, meta, keys = recurs_yaml(node, yaml, defs, meta, keys[:-1])
          return node, yaml, defs, meta, keys
        elif lkey == 'meta':
          yaml, meta = move_path(yaml, meta, keys)
          node, yaml, defs, meta, keys = recurs_yaml(node, yaml, defs, meta, keys[:-1])
          return node, yaml, defs, meta, keys
        else:
          node, yaml, defs, meta, keys = recurs_yaml(node, yaml, defs, meta, keys[:-1])
          return node, yaml, defs, meta, keys
    else:
      lkey = keys[-1]
      if lkey == 'all': 
        yaml, defs = move_path(yaml, defs, keys)
        node, yaml, defs, meta, keys = recurs_yaml(node, yaml, defs, meta, keys[:-1])
        return node, yaml, defs, meta, keys
      elif lkey == 'meta':
        yaml, meta = move_path(yaml, meta, keys)
        node, yaml, defs, meta, keys = recurs_yaml(node, yaml, defs, meta, keys[:-1])
        return node, yaml, defs, meta, keys
      else:
        node, yaml, defs, meta, keys = recurs_yaml(node, yaml, defs, meta, keys[:-1])
        return node, yaml, defs, meta, keys
  else: 
    for child in yaml.keys():
      keys.append(child)
      node, yaml, defs, meta, keys = recurs_yaml(yaml[child], yaml, defs, meta, keys)
      return node, yaml, defs, meta, keys

def parse_yaml(yaml):
  defs = {}
  meta = {}

  return recurs_yaml(None, yaml, defs, meta, [])

def linear_parse_yaml(yaml):
  defaults = {}
  meta = {}
  
  projects = yaml.keys()
  for project in projects:
    simulations = yaml[project].keys()
    keys = [project]
    pdict = yaml[project]
    get_defs_and_meta(yaml, defaults, meta, keys)
    if project == "all" or project == "meta":
      continue 
    for sim in simulations:
      anbundles = yaml[project][sim].keys()
      keys = [project, sim]
      abdict = pdict[sim]
      get_defs_and_meta(yaml, defaults, meta, keys)
      if sim == "all" or sim == "meta":
        continue 
      for abundle in anbundles:
        analyses = yaml[project][sim][abundle].keys()
        keys = [project, sim, abundle]
        adict = abdict[abundle]
        get_defs_and_meta(yaml, defaults, meta, keys)
        if abundle == "all" or abundle == "meta":
          continue 
        for analysis in adict:
          options = yaml[project][sim][abundle][analysis].keys()
          odict = adict[analysis]
          keys = [project, sim, abundle, analysis]
          get_defs_and_meta(yaml, defaults, meta, keys)
          if analysis == "all" or analysis == "meta":
            continue 
          for opt in odict:
            keys = [project, sim, abundle, analysis, opt]
            get_defs_and_meta(yaml, defaults, meta, keys)
            if opt == "all" or opt == "meta":
              continue 
  return yaml, defaults, meta


def make_and_check_ft(yaml,meta):
  '''This takes in the fully parsed yaml dictionary
  and ensures that the file tree the analyses need 
  is in place'''
  import os
  
  for project in yaml.iterkeys():
    pdict, pmeta = yaml[project], meta[project]['meta']
    a_path = pmeta['a_path']
    os.chdir(a_path)
    try:
      os.mkdir(project)
    except OSError:
      pass
    p_path = a_path + "/" + project
    os.chdir(p_path)
    for sim in pdict.iterkeys():
      sdict, smeta = get_dict_and_meta(pdict, sim)
      try:
        os.mkdir(sim)
      except OSError:
        pass
      s_path = p_path + "/" + sim
      os.chdir(s_path)
      for analysis in sdict.iterkeys():
        adict, ameta = get_dict_and_meta(sdict,analysis)
        try:
          os.mkdir(analysis)
        except:
          pass
        os.chdir(s_path)
