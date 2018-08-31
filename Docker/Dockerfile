FROM slzcc/supervisor:apt

RUN apt update && \
	apt install -y language-pack-zh-hans fonts-wqy-microhei fonts-wqy-zenhei xfonts-75dpi xfonts-base libfontenc1 libxfont1 xfonts-encodings xfonts-utils && \
	apt-get autoremove --purge --yes && \
    rm --force --recursive \
        /tmp/* \
        /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && \
    git clone https://gitee.com/shileizcc_admin/ResumeCRM.git /ResumeCRM

RUN pip install -r /ResumeCRM/package.txt

ENV MYSQL_DATABASE=resume \
    MYSQL_USER=resume \
    MYSQL_PASSWORD=resume \
    MYSQL_HOST="mysql" \
    MYSQL_PORT=3306 \
    SOLR_SERVER_URL="http://solr:8983/"

COPY . /ResumeCRM/
WORKDIR /ResumeCRM

EXPOSE 8088

CMD /ResumeCRM/Docker/docker-entrypoint.sh