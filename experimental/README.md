# ECS Experimental Definitions

ECS experimental definitions are changes and features which have reached [stage two](https://elastic.github.io/ecs/stages.html) in the ECS [RFC process](../rfcs)

Stage two changes only appear in the experimental artifacts in this directory, but aren't yet reflected in the official ECS documentation.
Note that stage three and four proposals do appear in the official ECS documentation.

These experimental changes to ECS are comprehensive but not necessarily final. They are also still subject to breaking changes.

## Schema Files

The [schemas](./schemas) directory contains the YAML files for the experimental field definitions. These are not always complete schemas. They can also be supplemental changes to be merged with the official schema spec, using the `--include` generator flag.

Example usage:

```sh
$ python scripts/generator.py --include experimental/schemas --out experimental
```

## Generated Artifacts

Various files generated based on the experimental ECS spec. The artifacts are generated using `make experimental` and published [here](./generated).
