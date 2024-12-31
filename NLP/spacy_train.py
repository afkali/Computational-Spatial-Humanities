# https://ner.pythonhumanities.com/03_01_create_ner_training_set.html
# https://ner.pythonhumanities.com/03_02_train_spacy_ner_model.html
# https://spacy.io/api/cli#init-config

import spacy
import pandas as pd
from spacy.tokens import DocBin
import spacy.cli
from sklearn.model_selection import train_test_split

df = pd.read_csv('NLP/last.csv')

TRAIN_DATA = []

# iterate over rows and format data
for index, row in df.iterrows():
    text = row['name']
    start, end, entity_type = eval(row['loc_col']) 
    entities = [(start, end, entity_type)]
    formatted_data = (text, {"entities": entities})
    TRAIN_DATA.append(formatted_data)

# loading the model like this because spacy is being a little b
spacy.cli.download("en_core_web_lg")
nlp = spacy.load("en_core_web_lg")

# splitting the data (we all know why the seed is 42)
train_data, validation_data = train_test_split(TRAIN_DATA, test_size=0.2, random_state=42)

# DocBin to store the training data
train_doc_bin = DocBin()

# DocBin to store the validation data
validation_doc_bin = DocBin()

# iterate over TRAIN_DATA and add it to DocBins
for text, annotations in train_data:
    doc = nlp.make_doc(text) 
    example = spacy.training.example.Example.from_dict(doc, annotations)
    train_doc_bin.add(example.reference)

#same for validation data
for text, annotations in validation_data:
    doc = nlp.make_doc(text) 
    example = spacy.training.example.Example.from_dict(doc, annotations)
    validation_doc_bin.add(example.reference)

train_data_file = 'NLP/train_dublin_streets.spacy'
validation_data_file = 'NLP/validation_dublin_streets.spacy'

train_doc_bin.to_disk(train_data_file)
validation_doc_bin.to_disk(validation_data_file)


'''
create base_config file, then:
python -m spacy init fill-config base_config.cfg config.cfg
train model:
python -m spacy train config.cfg --output ./NLP
# python -m spacy train config.cfg --paths.train C:/Users/husem/OneDrive/Dokumente/GitHub/CompSpaHumJoyce/NLP/train_dublin_streets.spacy --paths.dev C:/Users/husem/OneDrive/Dokumente/GitHub/CompSpaHumJoyce/NLP/validation_dublin_streets.spacy


'''
