#tiny script to check which model is being used by default

import spacy

nlp = spacy.load("en_core_web_trf")

transformer_component = nlp.get_pipe("transformer")

print(transformer_component.model.transformer.config)
