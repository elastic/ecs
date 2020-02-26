from generators import ecs_helpers
from os.path import join


def generate(ecs_nested, ecs_flat, out_dir):
    ecs_helpers.make_dirs(join(out_dir, 'ecs'))
    ecs_helpers.yaml_dump(join(out_dir, 'ecs/ecs_flat.yml'), ecs_flat)
    ecs_helpers.yaml_dump(join(out_dir, 'ecs/ecs_nested.yml'), ecs_nested)
