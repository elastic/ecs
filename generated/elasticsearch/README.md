# Sample Elasticsearch templates for ECS

Crafting the perfect Elasticsearch template is an art. But here's a good starting
point for experimentation.

When you're ready to customize this template to the precise needs of your use case,
please check out [USAGE.md](../../USAGE.md).

## Notes on index naming

This sample Elasticsearch template will apply to any index named `try-ecs-*`.
This is good for experimentation.

Note that an index following ECS can be named however you need. There's no requirement
to have "ecs" in the index name.

## Instructions

If you want to play with a specific version of ECS, check out the proper branch first.

```
git checkout 1.6
```

Load the template in Elasticsearch from your shell.

```bash
# Elasticsearch 7
curl -XPOST 'localhost:9200/_template/try-ecs' \
  --header "Content-Type: application/json" \
  -d @'generated/elasticsearch/7/template.json'

# or Elasticsearch 6
curl -XPOST 'localhost:9200/_template/try-ecs' \
  --header "Content-Type: application/json" \
  -d @'generated/elasticsearch/6/template.json'
```

Play from Kibana Dev Tools

```
# Look at the template you just uploaded 👀
GET _template/try-ecs

# index a document
PUT try-ecs-test
GET try-ecs-test
POST try-ecs-test/_doc
{ "@timestamp": "2020-10-26T22:38:39.000Z", "message": "Hello ECS World", "host": { "ip": "10.42.42.42"} }

# enjoy
GET try-ecs-test/_search
{ "query": { "term": { "host.ip": "10.0.0.0/8" } } }
```
