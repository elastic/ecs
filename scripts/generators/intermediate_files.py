from generators import ecs_helpers


def generate(ecs_nested, ecs_flat):
    ecs_helpers.yaml_dump('generated/ecs/ecs_flat.yml', ecs_flat)
    ecs_helpers.yaml_dump('generated/ecs/ecs_nested.yml', ecs_nested)
