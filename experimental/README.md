# ECS Experimental Definitions

ECS experimental definitions are changes and features which have reached [stage one](https://elastic.github.io/ecs/stages.html) in the ECS [RFC process](../rfcs)

Stage one changes only appear in the experimental artifacts in this directory but aren't yet reflected in the official ECS documentation.
Note that stage two and three proposals do appear in the official ECS documentation.

These experimental changes to ECS are comprehensive but not necessarily final. They are also still subject to breaking changes.

## Schema Files

The [experimental/schemas](./schemas) directory contains the YAML files for the experimental field definitions. These are not always complete schemas. They can also be supplemental changes to be merged with the official schema spec, using the `--include` generator flag.

If you use the ECS generator script as described in [USAGE.md](../USAGE.md) to maintain your custom index templates, here's how you can try these experimental changes in your project:

```sh
$ python scripts/generator.py --include experimental/schemas ../myproject/fields/custom/ \
    --out ../myproject/fields/generated
```

The above would include all experimental changes to ECS along with your custom fields and output the artifacts in `myproject/fields/generated`.

## Generated Artifacts

Various generated files based on the experimental ECS spec. The artifacts are generated using `make experimental` and published [here](./generated).
