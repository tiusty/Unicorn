===========
Cron jobs
===========

To access cron jobs type:

::
  
  sudo crontab -e 

Pull MLS homes every night
---------------------------

::
  
   0 0 * * * /home/ubuntu/work/Cocoon/config/scripts/update_homes > /home/ubuntu/work/crontab.log 2>&1
