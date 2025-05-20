#!/bin/bash
###########################################################
## Script for backup Mysql schemas in a weekly basis
#############################################################

umask 022

DIR_BACKUP="/backups"
FECHA=`date +'%Y%m%d'`
FECHA_I=`date +'%d-%m-%Y %H:%M:%S'`
FECHA_INI=`date +'%Y%m%d_%H%M'`
DIR_MYSQLDUMP="/usr/bin"
DIR_SHELL="/backups"

## cd $DIR_MYSQLDUMP
cd $DIR_SHELL

echo "***Start Backups Mysql - $FECHA"

###################### MySql schemas ####################

echo "*** Backup schemas MySql: $FECHA_I"

FILE_NAME6="$DIR_BACKUP/SCHEMA_NAME/register_$FECHA_INI.sql"
FILE_NAME_LOG6="$DIR_BACKUP/logs/register_$FECHA_INI.log"

FILE_NAME_FUN_PROC="$DIR_BACKUP/mediacion/storedprocedures_$FECHA_INI.sql"


################## ------ functions and stored procedures------------------------------ ###############
mysqldump -u root -pPasww --compact --no-create-info --where="db='SCHEMA_NAME/register_$FECHA_INI' AND name IN ('OBJECT_NAME1', 'OBJECT_NAME2','OBJECT_NAME2',
'OBJECT_NAME3'')"  --databases mysql --tables proc > $FILE_NAME_FUN_PROC


################## ------ DB VIEWS ESPECIFIC SCHEMA ------------ ###############
 mysql -u root -pPasww INFORMATION_SCHEMA --skip-column-names --batch -e "select table_name from INFORMATION_SCHEMA.tables where table_type = 'OBJECT_TYPE' and table_name in ('TABLE_NAME')" | xargs mysqldump -u root -pPasww SCHEMA > $FILE_VIEW.sql

FECHA_F=`date +'%d-%m-%Y %H:%M:%S'`

echo "***END Backup MySql schemas: $FECHA_F"
