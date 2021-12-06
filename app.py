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
import re
import csv


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

    def add_skills(self, skill):
        self.skills.add(skill)

    def set_email(self, email):
        self.email = email

    def __repr__(self):
        return f"name : {self.name} ; GPA : {self.gpa} ; skills: {self.skills} ; company names : {self.company_names}"


class Data:
    def __init__(self, loc):
        self.loc = loc
        self.skills = set()
        self.loadSkills()

    def loadSkills(self):
        with open(self.loc, "r") as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                self.skills.add(row[0].lower().strip())


class Parser:
    def __init__(self):
        self.data = Data("skills.csv")

    def parse_resume(self, text):
        resume = Resume()

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)

        # Assuming the GPA value is a single token (that is there is no space between the numbers and '.' )
        for token in doc:
            token_text = token.text.lower()
            if token_text == "gpa":
                resume.set_gpa(float(token.right_edge.text))
            elif token_text in self.data.skills:
                resume.add_skills(token_text)
            elif re.fullmatch(r"\w+@\w+.\w+", token_text) is not None:
                resume.set_email(token_text)

        name = ""
        min_index = float("inf")
        for ent in doc.ents:
            if ent.label_ == "PERSON" and ent.start < min_index:
                min_index = ent.start
                name = ent.text
        resume.set_name(name)

        return resume


# file_name = input("Enter the location of the resume (PDF)")
file_name = "../Selvaraaj_Joseph_Daniel_resume.pdf"

with pdfplumber.open(file_name) as pdf:
    first_page = pdf.pages[0]
    text = first_page.extract_text()
    parser = Parser()
    resume = parser.parse_resume(text)
    print(resume)
