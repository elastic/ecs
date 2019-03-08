def generate(ecs_nested, ecs_flat):
    ecs_helpers.yaml_dump('generated/ecs/fields_flat.yml', ecs_flat)
    ecs_helpers.yaml_dump('generated/ecs/fields_nested.yml', ecs_nested)
