rsbac-ff-shields
================

RSBAC FF runtime protection.

With this script and configuration files you can set files or directories to 
read only or any of the FF ff_flags values. Configuration format is json see example below.

usage::
       
  rsbac-ff-shields [-h] [-t] [-v] [--full {on,off,show}]

-h      show this help message and exit
-t      display time for execution
-v      make script noisily

Example configuration of a valid json::

  {
    "bin": {"paths": {"/bin": 1, "/tmp": 32}} ,
    "usr": {"paths-exclude": {"/usr": {exclude: ["share"]}}}
  }  

Explanation::

  "bin"           = key for command-line
  "paths"         = key word
  "/bin": 1       = directory set to read_only
  "/tmp": 32      = tmp directory set to no_execute 
  "paths-exclude" = key word
  "/usr"          = directory to set read_only
  "excludes"      = key word
  "share"         = director to exclude

Structur of Keywords::

  paths: {} 
  paths-excludes: { exclude: [], exclude-startswith: []}

The command-line key must be unique otherwise the last loaded is used.

Loadorder::

  00_general.json
  01_dev.json
  02_proc.json
  90_custom.json

The loading sequence is determined by the number which is at the beginning of the configuration file name.

Many predefined configuration files are prepared.
You can copy them to '/etc/rsbac/ff'::

  cp -v doc/example/etc/rsbac/ff/* /etc/rsbac/ff

Problem: boot or reboot
-----------------------

Storing RSBAC attribute on a virtual filesystem like '/proc' or '/sys' are not persistent.

Solution:
      
When using RSBAC UM module take a look at 'doc/examples/users/rsbac-ff-init'.
       
- create a ff_init user
- give ff_init user ff role 1

Copy prepared init start script at moment for gentoo::

   cp -v doc/examples/etc/init.d/rsbac-ff-init /etc/init.d/rsbac-ff-init

Create a file or copy::

   cp -v doc/examples/usr/bin/rsbac-ff-init /usr/bin/rsbac-ff-init
        
Content of /usr/bin/rsbac-ff-init::

   /usr/bin/rsbac-ff-shields --proc on --dev on --sys on

Add init script to runlevel for gentoo::
        
   rc-update add rsbac-ff-init default
        
When the system boot is finnish FF policies set on '/dev' and '/sys' and '/proc'.

