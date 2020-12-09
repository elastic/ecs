# Artifacts generated from ECS

Various kinds of files or programs can be generated directly based on ECS.

In this directory, you'll find the following:

* [beats/fields.ecs.yml](beats/fields.ecs.yml): The YAML field definition file
  used by **Beats to import ECS** in it's broader field schema. This might also
  be useful to community Beats maintainers.

* [csv/fields.csv](csv/fields.csv): A csv file you can use to import ECS field
  definitions in a **spreadsheet**. GitHub's csv rendering lets you filter
  the fields, too.

* [ecs/\*.yml](ecs/): These are the files to use when you need to **consume ECS
  programmatically**. The code generating the other ECS artifacts all operate on one
  of these two representations (documentation, csv, Elasticsearch template, etc).
  The two files are the fully fleshed out representation of ECS:
  default values are filled in, all fields being reused elsewhere are made explicit,
  additional attributes are computed.

* [elasticsearch/](elasticsearch#readme): Reference Elasticsearch **component templates**
  and a sample legacy all-in-one template to get started using ECS.
  Check out how to use them in [elasticsearch/README.md](elasticsearch#readme).
  Note that you can customize the content of these templates by following the
  instructions in [USAGE.md](/USAGE.md)

If you'd like to share your own generator with the ECS community, you're welcome
to look at our [contribution guidelines](/CONTRIBUTING.md), and then at the
generators in `scripts/generators`.
