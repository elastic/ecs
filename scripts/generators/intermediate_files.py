import os.path
from generators import ecs_helpers


def generate(ecs_nested, ecs_flat, out_dir):
    ecs_helpers.make_dirs(os.path.join(out_dir, 'ecs'))
    ecs_helpers.yaml_dump(os.path.join(out_dir, 'ecs/ecs_flat.yml'), ecs_flat)
    ecs_helpers.yaml_dump(os.path.join(out_dir, 'ecs/ecs_nested.yml'), ecs_nested)
