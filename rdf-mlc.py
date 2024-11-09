import spacy
import re
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import RDFS, XSD

# tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

def extract_triplets(text):
    doc = nlp(text)
    triplets = []

    for sent in doc.sents:
        subject = None
        relation = None
        object_ = None

        for token in sent:
            if token.dep_ == "nsubj" and subject is None:
                subject = token.text
            elif token.dep_ == "ROOT":
                relation = token.lemma_
            elif token.dep_ in ["dobj", "attr", "prep", "pobj"] and object_ is None:
                object_ = token.text

        if subject and relation and object_:
            triplets.append((subject, relation, object_))

    return triplets

def extract_modal_logic(text):
    modal_statements = []
    
    # Pattern for "If ... then ..." statements
    if_then_pattern = r"If (.*?) then (.*?)\."
    matches = re.findall(if_then_pattern, text)
    for match in matches:
        modal_statements.append(("IMPLIES", match[0].strip(), match[1].strip()))
    
    # Pattern for "X belongs to Y" statements
    belongs_to_pattern = r"(.*?) belongs to (.*?)\."
    matches = re.findall(belongs_to_pattern, text)
    for match in matches:
        modal_statements.append(("BELONGS_TO", match[0].strip(), match[1].strip()))

    return modal_statements

def create_rdf_graph(triplets, modal_statements):
    g = Graph()
    ns = Namespace("https://occurai.com")

    for subj, pred, obj in triplets:
        g.add((URIRef(ns + subj), URIRef(ns + pred), Literal(obj)))

    for modal_type, premise, conclusion in modal_statements:
        b = BNode()
        g.add((b, RDF.type, ns.ModalStatement))
        g.add((b, ns.modalType, Literal(modal_type)))
        g.add((b, ns.premise, Literal(premise)))
        g.add((b, ns.conclusion, Literal(conclusion)))

    return g

# Example usage
text = """
The Earth is round. The Sun is a star. 
If the Sun is shining then it is daytime. 
Planets belong to the solar system. 
If an object orbits the Sun then it is part of the solar system.
"""

triplets = extract_triplets(text)
modal_statements = extract_modal_logic(text)

print("Extracted Triplets:")
for t in triplets:
    print(t)

print("\nExtracted Modal Logic Statements:")
for m in modal_statements:
    print(m)

g = create_rdf_graph(triplets, modal_statements)
print("\nRDF Graph (in Turtle format):")
print(g.serialize(format="turtle"))
