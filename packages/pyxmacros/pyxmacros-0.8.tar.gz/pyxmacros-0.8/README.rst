pyxmacros
=========

Python library for creating system-wide macros on a linux machine. 
pyxmacros leverages the well known pyxhook library to connect to all X servers running on the machine and runs registered callback functions on desired keypress. Can also be triggered by lirc keypresses if desired.

usage
-----
::

  import xmacros

  def run_task(key):
      print "key pressed: %s" %str(key)

  if __name__ == "__main__":
      macro = xmacros()
      macro.register_action(key=190, mod=xmacros.MOD_ALT_L, callback=run_task)
    
      while True:
          pass
