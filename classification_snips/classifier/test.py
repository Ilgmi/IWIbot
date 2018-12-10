from __future__ import unicode_literals, print_function

import json
from pathlib import Path

from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.default_configs import CONFIG_DE

SAMPLE_DATASET_PATH = Path(__file__).parent / "dataset_de.json"
PERSIST_PATH = Path(__file__).parent / "persist_data"

with SAMPLE_DATASET_PATH.open(encoding="utf8") as f:
    sample_dataset = json.load(f)

load_resources("de")
nlu_engine = SnipsNLUEngine(config=CONFIG_DE)
nlu_engine.fit(sample_dataset)
#nlu_engine.persist(PERSIST_PATH)

text = "Hallo IWIBot ?"
parsing = nlu_engine.parse(text)
print(json.dumps(parsing, indent=2))

text = "Was gibt es heute zu essen in der Mensa?"
parsing = nlu_engine.parse(text)
print(json.dumps(parsing, indent=2))


text = "Wie wird das Wetter?"
parsing = nlu_engine.parse(text)
print(json.dumps(parsing, indent=2))

text = "Welches essen gibt es bei der Aktionstheke ? "
parsing = nlu_engine.parse(text)
print(json.dumps(parsing, indent=2))