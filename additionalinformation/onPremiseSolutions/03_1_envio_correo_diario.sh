#!/bin/bash
###########################################################

##!/bin/sh
## php /var/www/testdir/test.cron.php

## Script to execute PHP file to sent email notification for backups generated
#############################################################

umask 022

DIR_BACKUP="/backups/"
FECHA=`date +'%Y%m%d'`
FECHA_I=`date +'%d-%m-%Y %H:%M:%S'`
FECHA_INI=`date +'%Y%m%d_%H%M'`
DIR_MYSQLDUMP="/usr/bin"
DIR_SHELL="/backups/"

## cd $DIR_MYSQLDUMP
cd $DIR_SHELL

echo "***Start email - $FECHA"

#daily
  /usr/bin/php -f /var/www/.../enviocorreo_aud_diario.php


FECHA_F=`date +'%d-%m-%Y %H:%M:%S'`

echo "***End email - $FECHA_F"

