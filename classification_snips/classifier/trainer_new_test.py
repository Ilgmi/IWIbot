from trainer_new import SnipsNluTrainer
import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data.json"
print(DATA_PATH)

with DATA_PATH.open(encoding="utf8") as f:
    sample_dataset = json.load(f)

trainer_new = SnipsNluTrainer(sample_dataset)
#trainer_new.start_training()
trainer_new.rollback_nlu()
nlu_engine = trainer_new.get_nlu_engine()

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