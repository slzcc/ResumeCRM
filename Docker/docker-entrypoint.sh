#!/bin/bash

set -x 

#sed -i "s/'%s\*\=%s' % (name,\ value)/'%s\="%s"'\ % (name,\ value.encode('utf-8'))/" /usr/local/lib/python3.5/dist-packages/urllib3/fields.py

python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8088 &
curl http://127.0.0.1:8088/initialize/set_main
pkill python3

cat <<EOT > /etc/supervisord.conf

[supervisord]
nodaemon=true

[program:resume]
command=/bin/bash -c "python3 manage.py runserver 0.0.0.0:8088"
autorestart=true
startsecs=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0

[program:celery-worker]
command=/bin/bash -c "celery -A ResumeCRM worker -l debug --concurrency=1"
autorestart=true
startsecs=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0

[program:celery-beat]
command=/bin/bash -c "celery -A ResumeCRM beat -l info -S django"
autorestart=true
startsecs=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
EOT

exec /usr/bin/supervisord

