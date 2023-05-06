from elasticsearch import Elasticsearch

from blogController.models import Article
from elasticsearch.helpers import bulk

es = Elasticsearch(
    hosts=[{'host': 'localhost', 'scheme': 'http', 'port': 9200}],
    timeout=30,
)

try:
    es.indices.delete(index='articles')
except:
    pass

articles = Article.query.order_by(Article.date.desc()).all()

mappings = {
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "text", "analyzer": "english"},
        "intro": {"type": "text", "analyzer": "english"},
        "text": {"type": "text", "analyzer": "english"},
        "date": {"type": "date"},
    }
}

es.indices.create(index="articles", mappings=mappings)

for article in articles:
    doc = {
        'id': article.id,
        'title': article.title,
        'intro': article.intro,
        'text': article.text,
        'date': article.date,
    }

    es.index(index="articles", id=article.id, document=doc)

bulk_data = []
for art in articles:
    bulk_data.append(
        {
            "_index": "articles",
            "_id": art.id,
            "_source": {
                'title': art.title,
                'intro': art.intro,
                'text': art.text,
                'date': art.date,
            }
        }
    )
bulk(es, bulk_data)

es.indices.refresh(index="articles")
es.cat.count(index="articles", format="json")


def search_article(query_article):
    resp = es.search(
        index="articles",
        body={
            "query": {
                "match": {
                    "title": {
                        "query": query_article,
                        "fuzziness": "2"  # Здесь указываем максимальное расстояние Левенштейна (по умолчанию 2)
                    }
                }
            },
        }
    )

    hits = resp["hits"]["hits"]
    for hit in hits:
        return hit["_id"]

# docker run --rm -p 9200:9200 -p 9300:9300 -e "xpack.security.enabled=false" -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.3.3
