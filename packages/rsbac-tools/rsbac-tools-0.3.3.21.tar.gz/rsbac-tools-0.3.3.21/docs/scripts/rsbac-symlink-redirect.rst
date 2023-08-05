rsbac-symlink-redirect
----------------------

usage::
 
  rsbac-symlink-redirect [-h] [-v] 
                [-m {ip,uid,mac,rc-role}]
                [--ip-range {1,2,3,4}] 
                [-d tmp directory] 
                [{on,off,show}]


{on,off,shw}            toggle symlink redirection on or off or show status
 
-h                      show this help message and exit
-v                      show the command thats executed
-m                      {ip,uid,mac,rc-role}  set module if is active
--ip-range              {1,2,3,4}  must set when -m ip and status is on
-d                      tmp directory to use

.. note::

  When active or change the symlink redirect the users have to relogin. 
  Otherwise the gpg-agent or pulseadio or any service stored runtime information in 
  user tmp directory are not available anymore.

To create the tmpdirectory based on uid you can create a script.

Content for /etc/profile.d/rsbac-symlink-redirect-tmp.sh::

  if [ ! -d "/tmpdirs/tmp$UID" ]; then
      mkdir /tmpdirs/tmp$UID &&  chmod 700 /tmpdirs/tmp$UID
  fi

Copy::

  cp docs/example/etc/profile.d/rsbac-symlink-redirect-tmp.sh /etc/profile.de
 
After next login its create automatic the user tmp directory.

Fix::

  modules based tmp dir creation
