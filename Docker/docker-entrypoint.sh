#!/bin/bash

set -e

# https://docs.docker.com/compose/startup-order/
until mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -h mysql -e 'use resume;'; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"

python3 manage.py migrate

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