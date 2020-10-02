# ECS Experimental Definitions

ECS experimental definitions are changes and features which have been merged as [stage two](https://elastic.github.io/ecs/stages.html) in the ECS [RFC process](../rfcs), but they have not yet advanced stage three. These initial field definitions are comprehensive but not necessarily complete. They are also still subject to breaking changes or being removed in any future version.

This directory provides a location for these experimental field definitions and generated artifacts.

## Schema Files

The [schemas](./schemas) directory contains the YAML files for the experimental field definitions. These are not complete schemas themselves, but are settings meant to merge with the official schema spec using the `--include` generator flag.

Example usage:

```sh
$ python scripts/generator.py --include experimental/schemas --out experimental
```

## Generated Artifacts

Various files generated based on the experimental ECS spec. The artifacts are generated using `make experimental` and published [here](./generated).
