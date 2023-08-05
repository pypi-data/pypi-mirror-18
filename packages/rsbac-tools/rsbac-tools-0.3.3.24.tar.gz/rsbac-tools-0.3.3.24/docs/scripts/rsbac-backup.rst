rsbac-backup
------------

Info: Modules list is just an example depends on which modules are enabled.

 
usage:: 
  rsbac-backup [-h] [-v] [-t] [-b] [--full] 
                [--auth] [--cap] [--ff] [--general] [--jail] [--log]
                [--net] [--pax] [--reg] [--res] [--udf] [--um]

RSBAC attributes backup.

optional arguments::
  -h, --help            show this help message and exit
  -v, --verbose         Make the script verbose.
  -t, --time            Print time to execute.

options for backup::
  -b, --backup-directory  
                        Set backup directory for storing backup. Default is cwd/backup
  --full                Set full backup. This include all modules listed below.

module list::
  --auth                backup AUTH
  --cap                 backup CAP
  --ff                  backup FF
  --general             backup GENERAL
  --jail                backup JAIL
  --log                 backup LOG
  --net                 backup NET
  --pax                 backup PAX
  --reg                 backup REG
  --res                 backup RES
  --udf                 backup UDF
  --um                  backup UM

