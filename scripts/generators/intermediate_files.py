import yaml


def generate(ecs_nested, ecs_flat):
    with open('generated/ecs/fields_flat.yml', 'w') as outfile:
        yaml.dump(ecs_flat, outfile, default_flow_style=False)

    with open('generated/ecs/fields_nested.yml', 'w') as outfile:
        yaml.dump(ecs_nested, outfile, default_flow_style=False)
