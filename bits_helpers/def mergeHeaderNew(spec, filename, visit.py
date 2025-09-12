import pprint
import yaml
import hashlib
import sys
import os
import re
import platform

from os.path import exists, basename, join, isdir, islink
from glob import glob
from datetime import datetime
from collections import OrderedDict
from shlex import quote

from bits_helpers.cmd import getoutput
from bits_helpers.git import git
from bits_helpers.log import error, warning, dieOnError, debug
from bits_helpers.utilities import yamlLoad, yamlDump, getConfigPaths

def getGeneratedPackages(configDir):
  print("The configDir is %s" % configDir)
  pkgs = {}
  pkgDirs = getConfigPaths(configDir)
  print("The package directories are %s" % pkgDirs)
  exit (1)
  for pkgdir in pkgDirs:
    for vp in [x.split(os.sep)[-2] for x in  glob(join(pkgdir,"*","packages.py"))]:
      sys.path.insert(0,join(pkgdir, vp))
      pkg = __import__("packages")
      pkg.getPackages(pkgs, pkgdir)
      sys.modules.pop('packages')
      x=sys.path.pop(0)
  return pkgs
getGeneratedPackages(os.environ.get("BITS_REPO_DIR"))

#pprint.pprint(generatedPackages)
repoDir=os.environ.get("BITS_PATH")
print("The repoDir is %s" % repoDir)
# def getNewGeneratedPackages(configDir):
#     pkgs = {}
#     pkgDirs = getConfigPaths(configDir)
#     for pkgdir in pkgDirs:
#         repo_key = repoDir
#         pkgs.setdefault(repo_key, {})
#         for vp in [x.split(os.sep)[-2] for x in glob(join(pkgdir, "*", "packages.py"))]:
#             sys.path.insert(0, join(pkgdir, vp))
#             pkg = __import__("packages")
#             pkg.getPackages(pkgs[repo_key], pkgdir)
#             sys.modules.pop('packages')
#             sys.path.pop(0)
#     return pkgs
# newGeneratedPackages = getNewGeneratedPackages(os.environ.get("BITS_REPO_DIR"))
#pprint.pprint(newGeneratedPackages)