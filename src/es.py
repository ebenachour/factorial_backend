from config import AppConfig
from elasticsearch import Elasticsearch
from datetime import datetime

app_config = AppConfig()
parameters_config = app_config.load_config()
es = Elasticsearch(
    [
        "http://elasticsearch:9200"
    ]
)


def search_data(
    metric_name: str, filter_value: datetime, aggregation_interval: str
) -> dict:
    query = {
        "query": {"bool": {"must": [{"match": {"name": metric_name}}]}},
    }
    if aggregation_interval:
        interval = (
            "1m"
            if aggregation_interval == "minute"
            else "1h" if aggregation_interval == "hour" else "1d"
        )
        query.update( {
            "aggs": {
                "time_agg": {
                    "date_histogram": {"field": "timestamp", "interval": interval},
                    "aggs": {"avg_value": {"avg": {"field": "value"}}},
                }
            }
        })

    if filter_value:
        query["query"]["bool"]["filter"] = {
            "range": {"timestamp": {"gte": filter_value}}
        }
    response = es.search(index="metrics", body=query)
    return reformat_data(response)


def post_data(metric_name: str, value: float, timestamp: str) -> bool:
    # es_date_format = "yyyy-MM-dd'T'HH:mm:ss"
    format = '%Y-%m-%dT%H:%M'

    # converting the timestamp string to datetime object
    datetime_object = datetime.strptime(timestamp, format)
    es.index(
        index="metrics",
        body={"name": metric_name, "value": value, "timestamp": timestamp},
        refresh=True,
    )


def reformat_data(data):
    aggregation_data = data.get("aggregations", {}).get("time_agg", {}).get("buckets", []),
    hits = data.get('hits', {}).get('hits',[])
    search_hits = []
    for hit in hits:
        search_hit = {
            'id': hit['_id'],
            'name': hit['_source']['name'], # Include the _source part in an object
            'value': hit['_source']['value'],
            'timestamp': hit['_source']['timestamp']
        }
        search_hits.append(search_hit)
    return search_hits ,aggregation_data