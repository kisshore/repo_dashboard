#!/usr/bin/python

import os
import re

class LatestPackages:

  def __init__(self, env, repoPath):
    self.repoPath = repoPath
    self.env = env
    self.packages = {}

  def findComponentPath(self, path):
    component_path = [ x[0] for x in os.walk(path)
                   if ((len(os.path.basename(x[0])) > 1) and
                   not (os.path.basename(x[0]) == 'main')) ]
    print component_path
    return component_path

  def getComponentPackages(self, env, componentPaths):
    packagesList = {}

    for item in componentPaths:
      print 'finding latest version for: ', os.path.basename(item)
      envPackages = {}
      packagesVersion = os.listdir(item)
      packagesDup = [ x.split('_')[0] for x in packagesVersion ]
      packages = []
      [ packages.append(x) for x in packagesDup if x not in packages ]

      subPackage = {}
      for item1 in packages:
        subPackageList = []
        for x in packagesVersion:
          if item1 in x:
            subPackageList.append(x)
        subPackage[item1] = subPackageList

      latestPackages = {}
      for key, value in subPackage.iteritems():
        latestPackage = self.findLatestVersion(value)
        latestPackages[key] = latestPackage

      envPackages[env] = latestPackages
      packagesList[os.path.basename(item)] = envPackages

    return packagesList

  def findLatestVersion(self, packages):
    versionDup = []
    versions = []
    latestPackage = ''
    for item in packages:
      matchObj = re.search(r'(mos)(\d\d)', item)
      versionDup.append(matchObj.group(2))
    [ versions.append(x) for x in versionDup if x not in versions ]
    latestVersion = max(versions)

    for item in packages:
      if latestVersion in item:
        latestPackage = item

    return latestPackage

if __name__ == "__main__":
  #sysTest = LatestPackages('System Test', '/opt/mirror/stable/release/1508a/mos-6.1/pool/main')
  sysTest = LatestPackages('System Test', '/tmp/ks943g')
  componentPaths = sysTest.findComponentPath(sysTest.repoPath)
  packages = sysTest.getComponentPackages(sysTest.env, componentPaths)

  print packages
