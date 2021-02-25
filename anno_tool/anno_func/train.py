import spacy
import os
import json
import random
from api.glob_var import MODEL_PATH

def preprocess(json_file_path):
    try:
        training_data = []
        lines=[]
        with open(json_file_path, encoding = 'utf8') as f:
            lines = f.readlines()

        for line in lines:
            data = json.loads(line)
            #print(data)
            text = data['text']
            entities = []
            for annotation in data['labels']:
                #only a single point in text annotation.
                    #dataturks indices are both inclusive [start, end] but spacy is not [start, end)
                entities.append(annotation)
            training_data.append((text, {"entities" : entities}))
        return training_data
    except Exception as e:
        logging.exception("Unable to process " + JSON_FilePath + "\n" + "error = " + str(e))
        return None

def train_model(json_file_path, epochs=20):
    train_data = preprocess(json_file_path)
    spacy.prefer_gpu()
    if len(train_data)>=50:
        nlp = spacy.load(MODEL_PATH)
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
        with nlp.disable_pipes(*other_pipes):  # only train NER
            optimizer = nlp.resume_training()
            for itn in range(epochs):
                print("Starting iteration " + str(itn))
                random.shuffle(train_data)
                losses = {}
                index = 0
                batches = minibatch(train_data)
                for batch in batches:
                    text, annotations = zip(*batch)
                    try:
                        nlp.update(
                            text,  # batch of texts
                            annotations,  # batch of annotations
                            drop=0.25,  # dropout - make it harder to memorise data
                            sgd=optimizer,  # callable to update weights
                            losses=losses)
                    except Exception as e:
                        pass
                    
                print(losses)
        nlp.to_disk(MODEL_PATH)
    return "Model trained and saved"