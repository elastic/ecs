# Sample Elasticsearch templates for ECS

Crafting the perfect Elasticsearch template is an art. But here's a good starting
point for experimentation.

When you're ready to customize this template to the precise needs of your use case,
please check out [USAGE.md](../../USAGE.md).

The component index templates described below should be considered reference templates for ECS.

The composable template that brings them together, and the legacy all-in-one index
template should be considered sample templates. Both of them include all ECS fields,
which is great for experimentation, but is not actually recommended. The best practice
is to craft your index templates to contain only the field you needs.

## Index naming

These sample Elasticsearch templates will apply to any index named `try-ecs-*`.
This is good for experimentation.

Note that an index following ECS can be named however you need. There's no requirement
to have "ecs" in the index name.

## Instructions

Elasticsearch 7.8 introduced
[composable index templates](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-templates.html)
as the new default way to craft index templates.

The following instructions let you use either approach.

### Composable and component index templates

**Warning**: The artifacts based on composable templates are newly introduced in the ECS repository.
Please try them out and give us feedback if you encounter any issues.

If you want to play with a specific version of ECS, check out the proper branch first.
Note that the composable index templates are available in the ECS 1.7 branch or newer.

```
git checkout 1.7
```

First load all component templates in Elasticsearch. The following script creates
one reusable component template per ECS field set (one for "event" fields, one for "base" fields, etc.)

They will be named according to the following naming convention: `_component_template/ecs_{ecs version}_{field set name}`.

Authenticate your API calls appropriately by adjusting the username:password in this variable.

```bash
auth="elastic:elastic"
```

```bash
version="$(cat version)"
for file in `ls generated/elasticsearch/component/*.json`
do
  fieldset=`echo $file | cut -d/ -f4 | cut -d. -f1 | tr A-Z a-z`
  component_name="ecs_${version}_${fieldset}"
  api="_component_template/${component_name}"

  # echo "$file => $api"
  curl --user "$auth" -XPUT "localhost:9200/$api" --header "Content-Type: application/json" -d @"$file"
done
```

A component template for each ECS field set is now loaded. You could stop here and
craft a composable template with the settings you need, which loads only the ECS
fields your index needs via `composed_of`. You can look at [template.json](template.json) for an example.

If you'd like, you can load a sample composable template that contains all ECS fields,
for experimentation:

```bash
api="_index_template/try-ecs"
file="generated/elasticsearch/template.json"
curl --user "$auth" -XPUT "localhost:9200/$api" --header "Content-Type: application/json" -d @"$file"
```

#### Play from Kibana Dev Tools

```
# Look at the ECS component templates 👀
GET _component_template/ecs_*
# And if you created the sample index template
GET _index_template/try-ecs

# index a document
PUT try-ecs-test
GET try-ecs-test
POST try-ecs-test/_doc
{ "@timestamp": "2020-10-26T22:38:39.000Z", "message": "Hello ECS World", "host": { "ip": "10.42.42.42"} }

# enjoy
GET try-ecs-test/_search
{ "query": { "term": { "host.ip": "10.0.0.0/8" } } }
```

#### How to compose templates

Most event sources should include the ECS basics:

- base
- ecs
- event
- log

Most event sources should also include fields that capture "where it's happening",
but depending on whether you use containers or the cloud, you may want to omit some in this list:

- host (actually don't omit this one)
- container
- cloud

Depending on whether the index contains events captured by an agent or an observer, include one or both of:

- agent
- observer

Most of the other field sets will depend on which kind of documents will be in your index.

If the documents refer to network-related events, you'll likely want to pick among:

- client & server
- source & destination
- network
- dns, http, tls

If users are involved in the events:

- user
- group

And so on.

For a concrete example, an index containing your web server logs, should contain at least:

- base, ecs, event, log
- host, cloud and/or container as needed
- agent
- source, destination, client, server, network, http, tls
- user
- url, user\_agent

### Legacy index templates

If you want to play with a specific version of ECS, check out the proper branch first.

```
git checkout 1.6
```

Authenticate your API calls appropriately by adjusting the username:password in this variable.

```bash
auth="elastic:elastic"
```

Load the template in Elasticsearch from your shell.

```bash
# Elasticsearch 7
curl --user $"$auth" -XPOST 'localhost:9200/_template/try-ecs' \
  --header "Content-Type: application/json" \
  -d @'generated/elasticsearch/7/template.json'
```

#### Play from Kibana Dev Tools

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
