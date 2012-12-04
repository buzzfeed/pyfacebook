import traceback
import sys
import os
import datetime

class Fault(object):
  def __init__(self, message=None, tb=None ):
    if message is None:
      self.message = str( sys.exc_info( )[ 1 ] )
    else:
      self.message = message

    if tb is None:
      self.tb = traceback.extract_tb( sys.exc_info( )[ 2 ] )
    else:
      self.tb = tb

  def __unicode__( self ):
    "%s" % (self.message)


class FacebookException( Exception ):
  """
  A custom Facebook exception class

  """
  pass