# ResumeCRM

创建数据库:
```
mysql> create database resume character set 'UTF8';
mysql> grant all on resume.* to resume@'%' identified by 'resume';
```

安装启动包：
```
$ pip install -r package.txt
```

Django 创建 Models:
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

Django 创建 User:
```
$ python3 manage.py createsuperuser
```

启动 Django：
```
$ python3 manage.py runserver 8088
```

初始化：
```
$ curl http://127.0.0.1:8088/initialize/set_url_name_in_database
$ curl http://127.0.0.1:8088/initialize/set_primission_in_system_perimission
```