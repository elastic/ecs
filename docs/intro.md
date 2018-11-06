<!--

WARNING: README.md is generated based on the files under docs/
and the field descriptions in the YAML files under schemas/.

Therefore if you want to modify anything in this readme, please perform
your changes in these other locations, then run `make`.

See CONTRIBUTING.md for more details on setting up.

-->

**WARNING: THE MASTER BRANCH IS FOR WORK IN PROGRESS**

# Elastic Common Schema (ECS)

The Elastic Common Schema (ECS) defines a common set of fields for
ingesting data into Elasticsearch. A common schema helps you correlate
data from sources like logs and metrics or IT operations
analytics and security analytics.

ECS is still under development and backward compatibility is not guaranteed. Any
feedback on the general structure, missing fields, or existing fields is appreciated.
For contributions please read the [Contributing Guide](CONTRIBUTING.md).

<a name="ecs-version"></a>
# Versions

The latest version of ECS is [1.0.0-beta.1](https://github.com/elastic/ecs/tag/v1.0.0-beta.1).
You can browse past versions of ECS [here](https://github.com/elastic/ecs/releases)

Note that the master branch of this repository should never be considered an
official release of ECS.

# In this readme

* [Fields](#fields)
* [Use cases](#use-cases)
* [Implementing ECS](#implementing-ecs)
* [FAQ](#faq-ecs)

# <a name="fields"></a>Fields

ECS defines these fields.
