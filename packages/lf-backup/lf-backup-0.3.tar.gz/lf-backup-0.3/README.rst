LF Backup
=========

LF Backup stands for large file backup.

Installation
------------

RHEL / CentOS:

::

    sudo yum -y install epel-release
    sudo yum -y install python34 python34-setuptools python34-devel gcc postgresql-devel
    sudo easy_install-3.4 pip

Debian/Ubuntu:

::

    sudo apt-get install -y python3-dev libpq-dev

and then install lf-backup

::

    sudo pip3 install --upgrade pip
    sudo pip3 install lf-backup

Configuration
-------------

create a new swift container called "large-file-backup"

add the export statements for variables starting with ST\_ and the postgres authentication to config
file .lf-backuprc and set the permissions to 600

::

    > nano ~/.lf-backuprc​​
    > chmod 600 ~/.lf-backuprc
    > cat ~/.lf-backuprc
    export ST_AUTH=https://swiftcluster.domain.org/auth/v1.0
    export ST_USER=swift_account
    export ST_KEY=RshBXXXXXXXXXXXXXXXXXXXXX​
    export PGHOST=pgdb.domain.org
    export PGPORT=32048
    export PGDATABASE=storcrawldb
    export PGUSER=storcrawl_ro
    export PGPASSWORD= 

create a cron job /etc/cron.d/ running as root starting ca 7pm:

::

    > cat /etc/cron.d/lf-backup
    ## enabled on hostname xxx on 11-01-2016
    55 18 * * * root /usr/local/bin/lf-backup --sql "select * from table" \ 
               --prefix /fh/fast --container large-file-backup-fast >> /var/tmp/lf-backup-fast 2>&1

For modifications and change testing install a new system and install from local git folder

::

    > git clone https://github.com/FredHutch/lf-backup
    > rm -rf /usr/local/lib/python3.5/dist-packages/*; rm -rf /usr/local/bin/*
    > pip3 install -e ./lf-backup

    make changes in lf-backup and run again:

    > rm -rf /usr/local/lib/python3.5/dist-packages/*; rm -rf /usr/local/bin/*
    > pip3 install -e ./lf-backup

The script has the following features:

-  take a file list from a csv file or an SQL table and backup each file to object storage (e.g.
   swift)

-  if the file has an atime within the last x days (configurable) take an md5sum of that file and
   store the md5sum in an attribute / meta data called md5sum (not yet implemented)

-  check if the file is already in object store and do not upload if the file size and mtime is
   identical

-  notify a list of email-addresses after finishing. attach list of files that were uploaded; create
   one file list per file owner (username)

-  log every file that was uploaded to syslog, detailed logging of success and failure to enable
   storage team to monitor success / failure via splunk

-  bash script lf-backup is a wrapper for python script lfbackup.py, lf-backup sources and sets env
   vars with credentials and lfbackup.py only reads environments vars

-  main script lfbackup.py only uses swift functions in lflib.py.

-  segment size should be 1GB, segment container name should be .segments-containername, object type
   is slo, not dlo

-  backup with full path but replace prefix, for example a file
   /fh/fast/lastname\_f/project/file.bam would be copied to container/bucket bam-backup in account
   Swift\_\_ADM\_IT\_backup. The target path would be /bam-bucket/lastname\_f/project/file.bam a
   --prefix=/fh/fast removes the fs root path from the destination
