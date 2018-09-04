#!/bin/sh
mysql -u ${MYSQL_USER} -p${MYSQL_ROOT_PASSWORD} -h ${db_host} ${MYSQL_DATABASE} < /usr/src/app/dataseed/dev-seed.sql
exit 0 
