from trainer_new import SnipsNluTrainer
from cos_context import CosContext


import json
from pathlib import Path
ENGINE_PATH_NEW = Path(__file__).resolve().parents[1]/"engine/nlu_new"
ENGINE_PATH_OLD = Path(__file__).resolve().parents[1]/"engine/nlu_old"
ENGINE_PATH_NEW_ZIP = Path(__file__).resolve().parents[1]/"engine"
DATA_PATH = Path(__file__).resolve().parents[1]/"data.json"

with DATA_PATH.open(encoding="utf8") as f:
    sample_dataset = json.load(f)

trainer = SnipsNluTrainer(sample_dataset)
#trainer.start_training()
#nlu_engine = trainer.get_nlu_engine()
trainer.rollback_nlu()

#text = "Hallo IWIBot ?"
#parsing = nlu_engine.parse(text)
#print(json.dumps(parsing, indent=2))
