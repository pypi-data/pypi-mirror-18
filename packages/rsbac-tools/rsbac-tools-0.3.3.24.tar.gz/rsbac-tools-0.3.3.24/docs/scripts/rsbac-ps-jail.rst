rsbac-ps-jail
^^^^^^^^^^^^^

usage::

  rsbac-ps-jail [-h] [-t] [-p prog-name] [-j jail_id]

-h      show this help message and exit
-t      show execution time
-p      print only information about a single process
-j      print only processes with same jail_id


call::

  rsbac-ps-jail -t -p ping
   
output::
        
  ping                Pid: 17612   Jail Id: 79      Jail Ip: 0.0.0.0         
  Jail-Flags     : allow-inet-raw
  Jail-SCD-Modify: capability
  Time to execute: 0.03 seconds
