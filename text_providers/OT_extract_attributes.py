
from typing import Any, Callable, Dict, List, Union
#from AnoixoError import AnoixoError, ProbableBugError, ServerOverwhelmedError
#import app_constants
#import math
#from QueryResult import QueryResult
#from text_providers.TextProvider import TextProvider
#from TextQuery import TextQuery
#import json
#from text_providers import Nestle1904LowfatProvider_Config as Config
#import pandas as pd
import numpy as np
import pickle
text_dir = "../../../../STEPBible-Data/"
text_files = ["TOTHT - Tyndale OT Hebrew Tagged text Gen-Deu - TyndaleHouse.com STEPBible.org CC BY-NC.txt", \
"TOTHT - Tyndale OT Hebrew Tagged text Jos-Est - TyndaleHouse.com STEPBible.org CC BY-NC.txt", \
"TOTHT - Tyndale OT Hebrew Tagged text Job-Sng - TyndaleHouse.com STEPBible.org CC BY-NC.txt", \
"TOTHT - Tyndale OT Hebrew Tagged text Isa-Mal - TyndaleHouse.com STEPBible.org CC BY-NC.txt"]

allowed_attributes = [
            "attributes"
            "part of speech",
            "lexical form",
            "strong number",
            "state",
            "person", 
            "gender"]


"""
List of attributes:

Part of speech: adverb (D), conjunction (C) , preposition (R), particle (T), suffix (S), Noun, Verb
Lexical form: Extended Strongs (column)
Inflected form: introduces the question of what we want to do about vowel pointing, unusual forms
State: construct, abstract
Person: 1, 2, 3
Number: singular (
Gender: male, female, common (verbs), both (nouns)
"""

class bible_chunks:
    def __init__(self):
        #self.textname = 'Old Testament (Hebrew)'
        self.cache: Dict[str, Any] = {}
        self.book=[]
        self.chapter=[]
        self.verse=[]
        self.word_index=[]
        self.pointed_word=[]
        self.accented_word=[]
        self.morphology=[]
        self.strong_index=[]
        self.strong_heb=[]
        self.strong_eng=[]

    def add_chunks(self, passage_ref, point, accent, morphology, strong):
        if len(self.verse) == 0 or  not (self.verse[-1] == int(passage_ref.split(".")[1]) and self.word_index[-1] == int(passage_ref.split("-")[1].split(".")[0])):
            self.book.append(passage_ref.split(".")[0])
            self.chapter.append(int(passage_ref.split(".")[1]))
            self.verse.append(int(passage_ref.split(".")[2].split("-")[0]))
            self.word_index.append(int(passage_ref.split("-")[1].split(".")[0]))
            self.pointed_word.append(point)
            self.accented_word.append(accent)
            self.morphology.append(morphology.split("/"))
            s_index, s_heb, s_eng =[],[],[]
            for item in strong.split("/"):
                #print(passage_ref, "item", item) #debug
                if len(item) >1:
                    s_index.append(item.split("=")[0])
                    s_heb.append(item.split("=")[1])
                    s_eng.append(item.split("=")[2])
            self.strong_index.append(s_index)
            self.strong_heb.append(s_heb)
            self.strong_eng.append(s_eng)

    def print_words(self):
        print(" ".join([item for item in self.pointed_word]))

    def print_verses(self, index):
        # print out the verse that containing matched words (based on word index)
        items = [self.pointed_word[i] for i, x in enumerate(self.verse) if x == self.verse[index] and self.chapter[i]==self.chapter[index] and self.book[i]==self.book[index]]
        new_str = " ".join(items[:items.index(self.pointed_word[index])]) + " (" + items[items.index(self.pointed_word[index])] + ") " + " ".join(items[items.index(self.pointed_word[index]):])
        print(f"{self.book[index]} {self.chapter[index]}:{self.verse[index]} \t" + new_str)

    def extract_words(self):
        return [item for item in self.pointed_word]

    def extract_morphology(self):
        return [item for item in self.morphology]

    def extract_strong(self):
        return [item for item in self.strong_heb]

    def convert_to_dictionary(self):

        """
        # Here does the matching from raw chunks into the format we want, 
        # that can be directly covert to json format
        # -------------
        # Part of speech: adverb (D), conjunction (C) , preposition (R), particle (T), suffix (S), Noun, Verb
        # Lexical form: Extended Strongs (column)
        # Inflected form: introduces the question of what we want to do about vowel pointing, unusual forms
        # State: construct, absolute, sequential (c and verb)
        # Person: 1, 2, 3
        # Number: singular (i
        """

        dict_list = []
        pos_dict = {"D":"adverb","C":"conjunction","R":"preposition","T": "particle","S":"suffix","N": "noun","V":"verb", "A":"Adjective"}
        state_dict = {"c":"construct", "a": "absolute"}
        gender_dict = {"m":"male", "f":"female", "Nc": "common", "b":"both"}

        for i in range(len(self.book)):
            #pos_tag, state_tag, person_tag, gender_tag = "","","",""
            pos_tag, state_tag, person_tag, gender_tag = [],[],[],[]
            for item in self.morphology[i]:
                for key in pos_dict:
                    if key in item:
                        pos_tag.append(pos_dict[key])
                for key in state_dict:
                    if key in item:
                        if key == "c":
                            if item[-1] == "c":
                                state_tag.append(state_dict[key])
                        else:
                            state_tag.append(state_dict[key])
                for key in range(1,4):
                    if str(key) in item:
                        person_tag.append(str(key))
                for key in gender_dict:
                    if key in item:
                        gender_tag.append(gender_dict[key])
            if len(state_tag) == len(pos_tag):
                for j in range(len(state_tag)):
                    if state_tag[j] == 'construct' and pos_tag[j] == 'verb': #this condition is not too trival from the data
                        state_tag[j] = 'sequential' 
            #print(self.strong_heb[i])
            if pos_tag != []: 
                pos_tag = pos_tag if type(pos_tag)==str else ", ".join(pos_tag) 
            else:
                pos_tag = ""
            if state_tag != []: 
                state_tag = state_tag if type(state_tag)==str else ", ".join(state_tag)
            else:
                state_tag = ""
            if person_tag != []: 
                person_tag = person_tag if type(person_tag)==str else ", ".join(person_tag)
            else:
               person_tag = ""
            if gender_tag != []: 
               gender_tag = gender_tag if type(gender_tag)==str else ", ".join(gender_tag) 
            else:
               gender_tag = ""

            s_heb = self.strong_heb[i] if type(self.strong_heb[i])==str else ", ".join(self.strong_heb[i]) 
            s_index = self.strong_index[i] if type(self.strong_index[i])==str else ", ".join(self.strong_index[i]) 
            #s_index = ", ".join(self.strong_index[i])
            sub_dict = {"attributes": {
            "part of speech": pos_tag,
            "lexical form": s_heb,
            "strong number": s_index,
            "state": state_tag,
            "person": person_tag, 
            "gender": gender_tag
            }}
            print(self.pointed_word[i],self.morphology[i], sub_dict)
            dict_list.append(sub_dict)
        #print("testing")
        self.cache = dict_list

        return dict_list
   
    def extract_matched_queries(self, query_string: str, max_line):
        keys, values = [],[]
        match_index = []
        for item in query_string.split(" ; "):
            keys.append(item.split(":")[0])
            values.append(item.split(":")[1])
        for i in range(max_line):
            match = True
            for j in range(len(keys)):
                #print("keys[j]", keys[j])
                #print("values[j]", values[j])
                #print("self.cache",self.cache)
                #print("self.cache[i]",self.cache[i])
                #print("self.cache[i]['attributes']",self.cache[i]['attributes'])
                #print("self.cache[i]['attributes'][keys[j]]",self.cache[i]['attributes'][keys[j]])
                #print("values[j]", values[j])
                if values[j] not in self.cache[i]['attributes'][keys[j]]:
                    match = False
            if match:
                #print("match")
                match_index.append(i)

        return match_index
        
    def convert_to_json(self):
        print("testing")

    def _check_attributes(self, query) -> None:
        for sequence in query.sequences:
            for word_query in sequence.word_queries:
                for attribute in word_query.attributes:
                    if attribute not in allowed_attributes:
                        raise ProbableBugError(f'Attribute \'{attribute}\' not allowed')

    #def _sanitize(self, string: str) -> str:
    #    """
    #    Sanitizes a user-input string so it can be safely included in an XQuery query without the risk of injection
    #    attacks.
    #    :param string: The string to sanitize
    #    :return: The sanitized string
    #    """
    #    return string.replace('&', '').replace('\'', '’')

        

def read_text_to_query(text_files):
    OT_bible_chunks = bible_chunks()
    for i in range(len(text_files)):
        f = open(text_dir + text_files[i], "r")
        line = f.readline()
        while line:
            if len(line.split("\t")) == 6 and line.split("\t")[0] != "Ref in Heb":
                line = line.replace("\n","")
                items = line.split("\t")
                OT_bible_chunks.add_chunks(items[0],items[2],items[3],items[4],items[5])
                #line = ['Ref in Heb', 'Eng ref', 'Pointed', 'Accented', 'Morphology', 'Extended Strongs\n']
            line = f.readline() 
        f.close()
    
    # debug
    #a = OT_bible_chunks.extract_words()
    #print("words", a[:10])
    #a = OT_bible_chunks.extract_morphology()
    #print("words", a[:10])
    #a = OT_bible_chunks.extract_strong()
    #print("words", a[:10])
    OT_bible_chunks.convert_to_dictionary()
    #print("dict", a[:10])
    return OT_bible_chunks

   

#class OTProvider(textProvider):
#    def __init__(self):
#        self.cache: Dict[str, Any] = {}
#    def read_textfile(self, query_string: str) -> str:


"""
Here is the dry run to the senerio.
input_query is assume to be the queries selected by the user
the json file is expected to be the output
"""

def run_test():
   
    #input_query1 ="strong number:H1961"
    input_queries =["strong number:H9004", "part of speech:noun ; state:absolute ; gender:female"]
    
    max_lines = 5000 
    OT_bible_chunks = read_text_to_query(text_files)
    
    for input_query in input_queries:
        print("\n input_query =", input_query)
        
        match_index = OT_bible_chunks.extract_matched_queries(input_query, max_lines)
        for index in match_index:
            OT_bible_chunks.print_verses(index)


run_test()
