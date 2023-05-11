FROM mysql:8.0.25

RUN useradd -u 1000 mysql-admin-user
RUN chown -R mysql-admin-user:mysql-admin-user /var/lib/mysql

ENV MYSQL_ROOT_PASSWORD=pi31415926 \
    MYSQL_DATABASE=blog \
    MYSQL_USER=mysql-admin-user \
    MYSQL_PASSWORD=pi31415926

COPY data/mysql/init.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

CMD ["mysqld"]
