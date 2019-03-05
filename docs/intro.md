<!--

WARNING: README.md is generated based on the files under docs/
and the field descriptions in the YAML files under schemas/.

Therefore if you want to modify anything in this readme, please perform
your changes in these other locations, then run `make`.

See CONTRIBUTING.md for more details on setting up.

-->

WARNING: This is the master branch. The current release v1.0.0-beta2
can be found [here](https://github.com/elastic/ecs/tree/v1.0.0-beta2).

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

The master branch of this repository should never be considered an
official release of ECS. You can browse official releases of ECS
[here](https://github.com/elastic/ecs/releases).

Please note that when the README.md file and other generated files
(like schema.csv and template.json) are not in agreement,
the README.md should be considered the official spec.
The other two files are simply provided as a convenience, and may not always be
fully up to date.

# In this readme

* [Fields](#fields)
* [Use cases](#use-cases)
* [Implementing ECS](#implementing-ecs)
* [FAQ](#faq-ecs)
* [About ECS](#about-ecs)
* [Generated Files](#generated-files)

# <a name="fields"></a>Fields

ECS defines these fields.
