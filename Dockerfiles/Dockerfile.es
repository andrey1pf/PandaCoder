FROM docker.elastic.co/elasticsearch/elasticsearch:8.3.3

COPY elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
COPY log4j2.properties /usr/share/elasticsearch/config/log4j2.properties

USER elasticsearch

EXPOSE 9200 9300

CMD ["/usr/share/elasticsearch/bin/elasticsearch"]
