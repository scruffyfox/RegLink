#!/usr/bin/python

import sys, getopt, re, os, glob

VERSION = "0.1"

def main(argv):
   if len(argv) < 1:
      error()

   try:
      opts, args = getopt.getopt(argv, "hfsPv", ["help", "force", "symbolic", "phsyical", "verbose", "version"])
   except getopt.GetoptError:
      error()

   if len(opts) + len(args) > 0:
      for opt, arg in opts:
         if opt in ("-h", "--help"):
            print 'rs [-fsPv, --force --symbolic --physical --verbose --help --version] <source> <dest> [regex]...\n'
            print 'Example:  rs src/%1/to/%2/path /destination/path %1="/.*/" %2="/(path(s?))/"\n'
            print '[options]'
            print '  -f,   --force        Force override an existing file'
            print '  -s,   --symbolic     Create a symbolic link to a file'
            print '  -P,   --pysical      Make hard links directly to symbolic links'
            print '  -v,   --verbose      Print name of each linked file'
            print '  --help               Display this menu'
            print '  --version            Outputs version information and exit\n'
            print '[regex] use %n to reference regex strings in your <source> path'
            print '  %n "regex"\n'
            sys.exit(2)
         elif opt in ("--version"):
            print 'version %s by Callum Taylor 2014' % VERSION
            sys.exit(2)

      pathSource = args[0]
      destPath = args[1]
      regexParts = args[2:]
      pathParts = pathSource.split('/')

      regexPartPattern = re.compile("\%(.*)")
      globPathParts = []
      regexPathParts = []

      # build a list of path parts with the regex in place of its corrisponding %n 
      # also build a list of path parts with a glob [*] in place of %n
      for pathPart in pathParts:
         if regexPartPattern.match(pathPart) != None:
            regexPathParts.append(getPartForRegex(pathPart, regexParts))
            globPathParts.append('*')
         else:
            regexPathParts.append(pathPart)
            globPathParts.append(pathPart)

      regStr = '%s' % ("/".join(regexPathParts))
      filelist = glob.glob(r'%s' % ("/".join(globPathParts)))
      
      # loop through our found paths and filter in anything that matches our original sourcePath
      for file in filelist:
         if re.compile(regStr).match(file):
            print 'ln %s %s %s' % (" ".join(str(i[0]) for i in opts), file, destPath)
   else:
      print 'Unrecognised option(s) %s' % (args)
      sys.exit(2)

def getPartForRegex(needle, haystack):
   for hay in haystack:
      if hay.find(needle) > -1:
         return hay.split("=")[1]
   return None

def error():
   print 'rs <source> <dest> [options]'
   sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])