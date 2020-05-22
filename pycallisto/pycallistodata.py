import json
from importlib.resources import open_text

with open_text("pycallisto", "languages.json") as languages_JSON_file:
    LANGUAGES = json.load(languages_JSON_file)
