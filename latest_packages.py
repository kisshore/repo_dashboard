#!/usr/bin/python

import os
import re
import json

class LatestPackages:

  def __init__(self, env, repoPath):
    self.repoPath = repoPath
    self.env = env
    self.packages = {}

  def findComponentPath(self, path):
    component_path = [ x[0] for x in os.walk(path)
                   if ((len(os.path.basename(x[0])) > 1) and
                   not (os.path.basename(x[0]) == 'main')) ]
    return component_path

  def getComponentPackages(self, env, componentPaths):
    packagesList = {}

    for item in componentPaths:
      packagesVersion = os.listdir(item)
      packagesDup = [ x.split('_')[0] for x in packagesVersion ]
      packages = []
      latestPackages = {}
      [ packages.append(x) for x in packagesDup if x not in packages ]

      subPackage = {}
      for item1 in packages:
        subPackageList = []
        for x in packagesVersion:
          if x.startswith(item1+'_'):
            subPackageList.append(x)
        subPackage[item1] = subPackageList

      for key, value in subPackage.iteritems():
        latestPackage = self.findLatestVersion(value)
        latestPackages[key] = latestPackage

      packagesList[os.path.basename(item)] = latestPackages

    return packagesList

  def findLatestVersion(self, packages):
    versionDup = []
    versions = []
    latestPackage = ''
    for item in packages:
      matchObj = re.search(r'(mos)(\d\d)', item)
      if matchObj:
        versionDup.append(matchObj.group(2))
      else:
        matchObj = re.search(r'(mos)(\d)', item)
        versionDup.append(matchObj.group(2))
    [ versions.append(x) for x in versionDup if x not in versions ]
    latestVersion = max(versions)

    for item in packages:
      if latestVersion in item:
        latestPackage = item

    return latestPackage

if __name__ == "__main__":
  sysProdPackages = {}
  sysTest = LatestPackages('System Test', '/opt/mirror/stable/release/1508a/mos-6.1/pool/main')
  componentPaths = sysTest.findComponentPath(sysTest.repoPath)
  packages = sysTest.getComponentPackages(sysTest.env, componentPaths)
  sysProdPackages[sysTest.env] = packages

  prod = LatestPackages('Production', '/opt/repos/aptly/public/aicv2-mos-prod/mos-6.1/pool/main')
  componentPaths = prod.findComponentPath(prod.repoPath)
  packages = prod.getComponentPackages(prod.env, componentPaths)
  sysProdPackages[prod.env] = packages

  with open('aic-2.5-latest-packages.json', 'w') as outfile:
    json.dump(sysProdPackages, outfile)
