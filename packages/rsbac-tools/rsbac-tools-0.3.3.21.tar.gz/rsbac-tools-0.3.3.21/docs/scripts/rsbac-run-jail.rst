rsbac-run-jail
==============

RSBAC JAIL runtime protection.
Set a given program into a RSBAC JAIL.

usage::

  rsbac-run-jail [-h] [-v] [-d] [-c CONFIG] ...

positional arguments:
  program            program with arguments to execute

optional arguments:

-h      show this help message and exit
-v      enable verbosity
-d      do not execute the command
-c      config-file except as a valid json file in '/etc/rsbac/jail'


The script allows you to run a program in rsbac_jail and store the rsbac_jail arguments in a configuration file. The format of the configuration file is json.

Example configuration::

 {
   "jail-flags": ["allow-inet-raw""],
   "jail-ip": "0.0.0.0",
   "scd-modify": ["capability"]
 }

Example call::

  rsbac-run-jail -c ping /bin/ping heise.de

  is equal to 
        
  rsbac_jail -I 0.0.0.0 -M capability -r /bin/ping heise.de

Keywords for a configuration file:
  
===========  ==============
Keyword      excpeted Value
===========  ==============
chroot       string
jail-ip      string
jail-flags   list
max-caps     list
scd-get      list 
scd-modify   list
===========  ==============

Many predefined configuration files are prepared.

You can copy them to '/etc/rsbac/jail'::

  cp -v doc/example/etc/rsbac/jail/* /etc/rsbac/jail

If you like to put for example a program into a jail by search path then just copy::

  cp -v doc/example/profile.d/rsbac-jail-path.sh  /etc/profile.de/
  source /etc/profile 

With this action the first search path it now '/usr/local/jails'.

You  can copy samples now::
        
  mkdir /usr/local/jails
  cp -v doc/examples/usr/local/jails /usr/local/jails

An example file content /usr/local/jails/ping::

  rsbac-run-jail -c ping ping $*

Test::

  which ping
        /usr/local/jails/ping

Daemon can also put in a jail by just add rsbac-run-jail -c config-name before start-stop-daemon.

Example::  
        
  rsbac-run-jail -c ntpd start-stop-daemon --start --exec /usr/sbin/ntpd ...

ExitCodes:

  1   error on os.execp in RunJail

  10  not found rsbac_jail
  11  not found program to set in jail

  20  JailParams error
  21  JailFlags error
  22  JailMaxCaps error
  23  JailScdGet error
  24  JailScdModify error
