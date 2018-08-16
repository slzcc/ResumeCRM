FROM slzcc/supervisor:apt

RUN pip3 install --upgrade pip && \
    git clone https://gitee.com/shileizcc_admin/ResumeCRM.git /ResumeCRM

RUN pip install -r /ResumeCRM/package.txt

WORKDIR /ResumeCRM

ENV MYSQL_DATABASE=resume \
    MYSQL_USER=resume \
    MYSQL_PASSWORD=resume \
    MYSQL_HOST="172.17.0.2" \
    MYSQL_PORT=3306 \
    SOLR_SERVER_URL="http://172.17.0.3:8983/"

EXPOSE 8088