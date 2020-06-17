# Artifacts generated from ECS

Various kinds of files or programs can be generated directly based on ECS.

In this directory, you'll find the following:

* `beats/fields.ecs.yml`: The YAML field definition file used by Beats to import ECS in it's broader
  field schema.

* `csv/fields.csv`: A csv file you can use to import ECS field definitions
in a spreadsheet.

* `ecs/*.yml`: These are the files you should use, if you need to consume ECS
  programmatically. This repo's artifact generators all operate based off of one
  of these two representations (documentation, csv, Elasticsearch
  template, etc).
  The two files are the fully fleshed out representation of ECS:
  default values are filled in, all fields being reused elsewhere are made explicit,
  additional attributes are computed.

* `elasticsearch/{6,7}/template.json`: Sample Elasticsearch templates to get
  started using ECS. Check out how to use them in
  [generated/elasticsearch/README.md](elasticsearch).

If you'd like to share your own generator with the ECS community, you're welcome
to look at our [contribution guidelines](/CONTRIBUTING.md), and then at the
generators in `scripts/generators`.
