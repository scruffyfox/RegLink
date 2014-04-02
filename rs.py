#!/usr/bin/python

import sys, getopt

VERSION = "0.1"

def main(argv):
   if len(argv) < 1:
      error()

   try:
      opts, args = getopt.getopt(argv, "hf:P:v:", ["help", "force", "phsyical", "verbose", "version"])
   except getopt.GetoptError:
      error()

   if len(opts) + len(args) > 0:
      for opt, arg in opts:
         if opt in ("-h", "--help"):
            print 'rs [options]... <source> <dest> [regex]...\n'
            print 'Example:  rs.py src/%1/to/%2/path /destination/path %1="/.*/" %2="/(path(s?))/"\n'
            print '[options]'
            print '  -f,   --force        Force override an existing file'
            print '  -P,   --pysical      Make hard links directly to symbolic links'
            print '  -v,   --verbose      Print name of each linked file'
            print '  --help               Display this menu'
            print '  --version            Outputs version information and exit\n'
            print '[regex] use $n to reference regex strings in your <source> path'
            print '  $n "regex"'
         elif opt in ("--version"):
            print 'Version %s' % VERSION

      print 'options %s' % (opts)
      print 'args %s' % (args)
   else:
      print 'Unrecognised option(s) %s' % (args)
      sys.exit(2)

def error():
   print 'rs <source> <dest> [options]'
   sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])