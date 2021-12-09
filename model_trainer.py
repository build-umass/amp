import json
import spacy
from spacy.util import filter_spans
from spacy.tokens import DocBin
import plac

class Trainer:
    def prepare_data(self,json_path, write_path):
        train_data_set = DocBin()
        nlp = spacy.blank("en")
        with open(json_path, "r", encoding="utf8") as f:
            for line in f:
                record = json.loads(line)
                doc = nlp(record["content"])
                ents = []
                for ann in record["annotation"]:
                    for label in ann["label"]:
                        span = doc.char_span(ann["points"][0]["start"],ann["points"][0]["end"] + 1,label = label)
                        if span is not None:
                            ents.append(span)
                ents = filter_spans(ents)
                doc.ents = ents
                train_data_set.add(doc)

        train_data_set.to_disk(write_path)

    # def train(self, iters):
    #     ner = None
    #     if self.model.has_pipe("ner"):
    #         ner = self.model.get_pipe("ner")
    #     else:
    #         ner = self.model.add_pipe("ner", last=True)
    #
    #     for doc in self.train_data_set:
    #         for ent in doc.ents:
    #             print(ent.label_)


if __name__ == "__main__":
    trainer = Trainer()
    plac.call(trainer.prepare_data)
