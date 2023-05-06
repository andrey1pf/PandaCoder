FROM mysql:8.0.25

ENV MYSQL_ROOT_PASSWORD=pi31415926 \
    MYSQL_DATABASE=blog \
    MYSQL_USER=root \
    MYSQL_PASSWORD=pi31415926

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

CMD ["mysqld"]
