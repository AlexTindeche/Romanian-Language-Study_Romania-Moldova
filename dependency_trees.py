import numpy as np
import sqlite3

romanian_texts = {}
moldavian_texts = {}

conn = sqlite3.connect('news.db')
c = conn.cursor()

c.execute('SELECT * FROM romania')
rows = c.fetchall()
for row in rows:
    if row[4] not in romanian_texts:
        romanian_texts[row[4]] = []
    romanian_texts[row[4]].append(row[5])
    
c.execute('SELECT * FROM moldova')
rows = c.fetchall()
for row in rows:
    if row[4] not in moldavian_texts:
        moldavian_texts[row[4]] = []
    moldavian_texts[row[4]].append(row[5])

conn.close()


# Construct dependecy trees using spacy
import spacy


import spacy
nlp = spacy.load('xx_ent_wiki_sm')  # Load the multi-language model


# Assuming you have the IPython display tools installed for visualization
from spacy import displacy

# Function to process and display the dependency tree of the first text in each category
def display_dependency_trees(texts_dict):
    for category, texts in texts_dict.items():
        if texts:  # Check if there are texts in the category
            doc = nlp(texts[0])  # Process the first text of the category
            displacy.render(doc, style='dep', jupyter=True, options={'distance': 90})
            print(f"Category: {category}\nText: {texts[0][:50]}...")  # Print category and part of the text
            break  # Remove this if you want to visualize trees for more than one text per category

print("Dependency Trees for Romanian Texts:")
display_dependency_trees(romanian_texts)

print("\nDependency Trees for Moldavian Texts:")
display_dependency_trees(moldavian_texts)
