"""
Parse resume -> P
Give P as input to a ML Model
The model can be a classifier for classifying a resume to a project based on the project description
It can also be an recommender (Like k nearest neighbour) model which selects the top n candidates who are best fit to join build.
https://pdf.sciencedirectassets.com/280203/1-s2.0-S1877050920X00056/1-s2.0-S187705092030750X/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEIX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQCrfdwBJIu7xY6pD9SIazKqmLe36AU1KibmHG0ePBJtYAIhANi7BWD5qtlXOFd8JG%2BtAP6oMh54QBtQjnTQc7jtMknbKvoDCE4QBBoMMDU5MDAzNTQ2ODY1IgyVwm55NzPL8vKzsekq1wNB9rx1JvnDbpXb5ZHmcjCcFSCuzu2QfD6quhjNIjgjXerabkI1P52d%2F0%2FCjSm3YSMm6BRpdwgjim9nr3AGRtjQyS1pOKNkKyE3ld08mwIdBgXXEr1hA9QMcluz41kmZumI03mM0q6Xa0H3%2FBRQgGOVjPphLI72jrMIdt%2FPtJE6uHesW4Ao7uBXH%2FezHPDn5ht%2Fo2V0gFjwMWx%2BfnZ%2FMrenzgnxU0ZsuIBIV75Mp09x3WBCaoUFQEwdHr0WIpVjN37ZTycA6wxmwzZF%2FgvT9oUIuNIK43AgqehGaq1ywcPEqqK%2B6Pz%2BBAg48JSp%2FfhB5FtAxYwL2rmdWRIFBSCxOYRloNTj5fCAVXTTLXzgMZ1WnhmZEApk%2BCC2MUu71OcDLSS%2FTZ%2B4ga4i6OMVHePn8ahFXDSJG2aBPzL1vMnmLulwbtUDuhmkJp7NsGGT8eKiJLRIGXU8eVcbxmqwa7l8Ve%2BNkK9kMxvNkPksROnRkl5xbJcbZRketW55mSebZi5KCjULD2eTi2F85xjrn%2BOd3RDHMPYywqyU%2Fh%2Bi32K32wyd0fO8iXXU%2Bwe5inxn7yAhulhP05esf6dXzgt%2FWp7wREaPW17s6CcXDf098lljfFHEHXlSuB%2Fb6ikwoKX1jAY6pAE7DWmXXZNdzj1p4k1SweaeCR1JZ654mVZQC0d7lQ3qaadTMAyunaT6JYeuAxFu0flPVgmx31gqHa%2FMe6JTbyrZ3%2BdgSD7pGAH6AdG90t5aujDjo27G3nUaaPf24mVH0UmusBXMi4J3XQLBcxIRWda3VJjCHdDHUUGG1jCL5gq7g60PBBmEDoduZjuEgde9Ahi953fmu%2BOP%2BfzT682QHu%2Bnd%2FIgsA%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20211123T220834Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYZA53DL72%2F20211123%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=0964d61a10404559e3a0ddb6c2bed92755bd49c595445ead04e3043977e51228&hash=c90ac608380b18548a8dd40b59e285d47b1d7e37640fdb7633fe8bff550866e8&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S187705092030750X&tid=spdf-21b5a3db-caa0-46b4-8c17-5566741c88e1&sid=41d3578c8641f649ac396f39891b90c0dd01gxrqa&type=client
"""

'''
name
email
Skills
GPA
companies names
'''

import pdfplumber
import spacy
import csv
import plac
import json
import pandas as pd


class Resume:
    def __init__(self):
        self.gpa = -1
        self.skills = set()
        self.email = ""
        self.name = ""
        self.company_names = []

    def set_name(self, name):
        self.name = name

    def set_gpa(self, gpa):
        self.gpa = gpa

    def add_company(self, company):
        self.company_names.append(company)

    def add_skill(self, skill):
        self.skills.add(skill)

    def set_email(self, email):
        self.email = email

    def __repr__(self):
        return f"name : {self.name} ; GPA : {self.gpa} ; skills: {self.skills}; email: {self.email} ; company names : {self.company_names} "


class DataPoint:
    def __init__(self, text):
        self.content = text
        self.annotations = []

    def annotation_maker(self, label, text, start, end):
        return {"label": label, "point": {"start": start, "end": end, "text": text}}

    def set_name(self, name, start, end):
        self.annotations.append(self.annotation_maker("name", name, start, end))

    def set_gpa(self, gpa, start, end):
        self.annotations.append(self.annotation_maker("gpa", gpa, start, end))

    def add_company(self, company, start, end):
        self.annotations.append(self.annotation_maker("company", company, start, end))

    def add_skill(self, skill, start, end):
        self.annotations.append(self.annotation_maker("skill", skill, start, end))

    def set_email(self, email, start, end):
        self.annotations.append(self.annotation_maker("name", email, start, end))

    def to_json(self):
        return json.dumps({"content": self.content,
                           "annotations": self.annotations})


class DataCollector:
    def __init__(self):
        self.db = set()

    def add_data_point(self, data):
        self.db.add(data)

    def write_out(self, path="./data_collection/resumes.json"):
        with open(path, "a") as f:
            for data in self.db:
                f.write(data.to_json())
                f.write("\n")


class Data:
    def __init__(self, loc,col):
        self.loc = loc
        self.set = set()
        self.load(col)

    def load(self,col_name):
        df_chunks = []
        for chunk in pd.read_csv(self.loc,encoding="utf8",chunksize=1000):
            df = chunk.dropna()
            df_chunks.append(df[col_name].str.lower())
        df = pd.concat(df_chunks)
        self.set = set(df.unique())
        print("Loaded")

        # with open(self.loc, "r", encoding="utf8") as f:
        #     csv_reader = csv.reader(f)
        #     for row in csv_reader:
        #         self.set.add(row[col].lower().strip())

    def __iter__(self):
        return iter(self.set)


class Parser:
    def __init__(self, skills_path="./assests/skills_2.csv", companies_path="./assests/companies.csv"):
        self.skills = Data(skills_path,"name")
        self.companies = Data(companies_path,"name")
        self.data_collector = DataCollector()

    def parse_gpa(self, doc, index):
        if index >= len(doc):
            return float("-inf"), -1
        if doc[index].like_num:
            return float(doc[index].text), index
        return self.parse_gpa(doc, index + 1)

    def parse_resume(self, resume_path="../resume.pdf"):
        with pdfplumber.open(resume_path) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            resume = self.parse_resume_text(text)
            print(resume)

    def parse_resume_text(self, text):
        resume = Resume()
        data_point = DataPoint(text)
        print("Started")
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        # Assuming the GPA value is a single token (that is there is no space between the numbers and '.' )
        for i,token in enumerate(doc):
            token_text = token.text.lower()
            start, end = token.idx, token.idx + len(token)
            if token_text == "gpa":
                gpa, index = self.parse_gpa(doc, token.i + 1)
                resume.set_gpa(gpa)
                token = doc[index]
                start, end = token.idx, token.idx + len(token)
                data_point.set_gpa(gpa, start, end)
            elif token_text in self.skills:
                resume.add_skill(token_text)
                data_point.add_skill(token_text, start, end)
            elif token_text in self.companies:
                resume.add_company(token_text)
                data_point.add_company(token_text, start, end)
            elif token.like_email:
                resume.set_email(token_text)
                data_point.set_email(token_text, start, end)
            print(i)

        name = ""
        start, end = -1, -1
        min_index = float("inf")
        for ent in doc.ents:
            if ent.label_ == "PERSON" and ent.start < min_index:
                min_index = ent.start
                name, start, end = ent.text, ent.start, ent.end
        resume.set_name(name)
        data_point.set_name(name, start, end)

        self.data_collector.add_data_point(data_point)
        return resume

    def write(self):
        self.data_collector.write_out()


if __name__ == "__main__":
    parser = Parser()
    plac.call(parser.parse_resume)
    parser.write()
