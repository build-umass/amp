import json
import spacy
from spacy.util import filter_spans
from spacy.tokens import DocBin
import plac
import re


class Trainer:
    @staticmethod
    def prepare_data(json_path="./assests/train.json", write_path="./corpus/train.spacy"):
        train_data_set = DocBin()
        invalid_token = re.compile(r"\s")
        nlp = spacy.blank("en")
        with open(json_path, "r", encoding="utf8") as f:
            for line in f:
                record = json.loads(line)
                text = record["content"]
                doc = nlp(text)
                ents = []
                for ann in record["annotation"]:
                    start = ann["points"][0]["start"]
                    end = ann["points"][0]["end"] + 1
                    for label in ann["label"]:
                        while start < len(text) and invalid_token.match(text[start]):
                            start += 1
                        while end > 1 and invalid_token.match(text[end - 1]):
                            end -= 1
                        if start <=end:
                            span = doc.char_span(start, end, label=label)
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
    plac.call(Trainer.prepare_data)
