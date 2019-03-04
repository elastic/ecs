# Sample Elasticsearch templates for ECS

Crafting the perfect Elasticsearch template is an art. But here's a good starting
point for experimentation.

## Instructions

Load the template from your shell

```bash
# Elasticsearch 7
curl -XPOST 'localhost:9200/_template/ecs-test' --header "Content-Type: application/json" \
  -d @'generated/elasticsearch/7/template.json'

# or Elasticsearch 6
curl -XPOST 'localhost:9200/_template/ecs-test' --header "Content-Type: application/json" \
  -d @'generated/elasticsearch/6/template.json'
```

Play from Kibana Dev Tools

```
# 👀
GET _template/ecs-test

# index
PUT ecs-test
GET ecs-test
POST ecs-test/_doc
{ "@timestamp": "2019-02-26T22:38:39.000Z", "message": "Hello ECS World", "host": { "ip": "10.42.42.42"} }

# enjoy
GET ecs-test/_search
{ "query": { "term": { "host.ip": "10.0.0.0/8" } } }
```
