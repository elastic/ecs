import yaml
import glob
import copy

if __name__ == "__main__":

    fields = []
    for path in sorted(glob.glob("schemas/*.yml")):

        with open(path) as f:
            f = yaml.load(f.read())
            fields = fields + f

    base_index = -1
    for i in range(len(fields)):
        if fields[i]["name"] == "base":
            # Move base keys to the top level
            for vv in fields[i]["fields"]:
                fields.append(copy.deepcopy(vv))

            base_index = i

    # Delete original base keys
    del fields[base_index]

    yml = [
        {
            "key": "ecs",
            "title": "ECS",
            "description": "ECS fields.",
            "fields": fields,
        }
    ]

    with open('fields.yml', 'w') as f:
        yaml.dump(yml, f, default_flow_style=False, indent=4)
