#!/bin/bash

set -e

# https://docs.docker.com/compose/startup-order/
host=$MYSQL_HOST

until MYSQL_ROOT_USER=$MYSQL_ROOT_USER MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -h "$host" -e 'show databases;'; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"


isDatabase=`mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -h "$host" -e "show databases;" | egrep "^$MYSQL_DATABASE$" | wc -l`

if [[ $isDatabase -eq 0 ]]; then 
  echo "NOT Database, Perform create!"
  mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -h "$host" -e "create database $MYSQL_DATABASE character set 'UTF8'"
  mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -h "$host" -e "grant all on $MYSQL_DATABASE.* to $MYSQL_USER@'%' identified by '$MYSQL_PASSWORD'"
fi

python3 manage.py makemigrations

python3 manage.py migrate

isDatabaseTable=`mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -h "$host" -e "use $MYSQL_DATABASE; select * from repository_userprofile;" | wc -l`

if [[ $isDatabaseTable -eq 0 ]]; then 
  	nohup python3 manage.py runserver 0.0.0.0:8088 >> /var/log/resumecrm.log 2>&1 &
	until curl -fsSL "http://localhost:8088/user/login" >/dev/null; do
	  >&2 echo "Waiting to start..."
	  sleep 1
	done
	curl http://127.0.0.1:8088/initialize/set_main && pkill python3
fi

cat <<EOT > /etc/supervisord.conf

[supervisord]
nodaemon=true

[program:resume]
autorestart = false
autostart = true
command=/bin/bash -c "python3 manage.py runserver 0.0.0.0:8088"
startsecs=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0

[program:celery-worker]
autorestart = false
autostart = true
command=/bin/bash -c "celery -A ResumeCRM worker -l debug --concurrency=1"
startsecs=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0

[program:celery-beat]
autorestart = false
autostart = true
command=/bin/bash -c "celery -A ResumeCRM beat -l info -S django"
startsecs=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
EOT

exec /usr/bin/supervisord