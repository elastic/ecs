import yaml

import schema_reader

def intermediate_files():
    (ecs_nested, ecs_fields) = schema_reader.load_ecs()
    with open('generated/ecs/fields_flat.yml', 'w') as outfile:
        yaml.dump(ecs_fields, outfile, default_flow_style=False)
    with open('generated/ecs/fields_nested.yml', 'w') as outfile:
        yaml.dump(ecs_nested, outfile, default_flow_style=False)

if __name__ == '__main__':
    intermediate_files()
