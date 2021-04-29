import jinja2
import json
import os
import sys


def save_ndjson(filename, list_of_objs):
    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"
    with open(filename, open_mode) as file_obj:
        for obj in list_of_objs:
            file_obj.write(json.dumps(obj, sort_keys=True) + "\n")


def save_asciidoc(filename, template, data):
    TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=TEMPLATE_DIR)
    )
    template = env.get_template(template)
    with open(filename, "w") as file_obj:
        file_obj.write(template.render(data))


def default_detection_rule():
    return {
        "from": "now-1d",
        "interval": "1d",
        "risk_score": 42,
        "severity": "high",
        "type": "query"
    }
