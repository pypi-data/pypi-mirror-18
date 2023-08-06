#!/usr/bin/env python

import sys
import imp

#import Services

## Checking if Utilities module exists
##  Otherwise, force it find it assuming this module
##  is in /Services/Sniffer/NetworkSniffer.py
try:
  from Services.ContextService import ContextProvider
except ImportError:
  currentPath = sys.path[0]
  path = ['/'.join(currentPath.split('/')[:-1])+'/Services/ContextService/']
  name = 'ContextProvider'
  print "Exporing libraries from [%s]"%name
  try:
    fp = None
    (fp, pathname, description) = imp.find_module(name, path)
    ContextProvider = imp.load_module(name, fp, pathname, description)
  except ImportError:
    print "  Error: Module ["+name+"] not found"
    sys.exit()
  finally:
    # Since we may exit via an exception, close fp explicitly.
    if fp is not None:
      fp.close()
      fp=None
    #print "  Imported libraries for [%s]"%name

if __name__ == '__main__':
  if len(sys.argv) != 2:
      print "usage: service_context.py"
      raise SystemExit
  ContextProvider.main(sys.argv[1])
  