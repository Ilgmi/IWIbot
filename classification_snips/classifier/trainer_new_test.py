from trainer_new import SnipsNluTrainer


test_bin_data = b"abc123+=$"
trainer = SnipsNluTrainer("")

#test de&serializable funktions
def test_serialisation_data(data):
    serialisable = trainer.serializable_engine(data)
    return trainer.deserializable_engine(serialisable) == data

print(test_serialisation_data(test_bin_data))

