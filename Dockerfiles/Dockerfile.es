FROM docker.elastic.co/elasticsearch/elasticsearch:8.3.3

ENV xpack.security.enabled=false
ENV discovery.type=single-node
ENV JVM_OPTS="-Xms256m -Xmx256m"
ENV bootstrap.memory_lock=true

EXPOSE 9200 9300

CMD ["elasticsearch"]