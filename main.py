# main_loop.py

import spacy
import re
from neo4j_prolog_file import create_neo4j_connection, create_neo4j_graph, query_relationship, get_all_node_names
# from prolog_file import query_relationship

def add_custom_entity_rules(nlp):
    lowercase_names = ["ibtisam", "salman", "mahnoor", "mustafa", "ayesha", "eman", "saneeaa", "aimen", "haider", "rehan"]
    for name in lowercase_names:
        nlp.tokenizer.add_special_case(name, [{"ORTH": name.lower()}])

    # Add special cases for relationship terms
    relationship_terms = ["uncle", "aunt", "brother", "sister"]
    for term in relationship_terms:
        nlp.tokenizer.add_special_case(term, [{"ORTH": term}])

    # Define patterns to match lowercase names
    patterns = [{"label": "PERSON", "pattern": [{"LOWER": {"IN": lowercase_names}}]}]

    # Add a new rule to the entity recognizer
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)

nlp = spacy.load("en_core_web_sm")
add_custom_entity_rules(nlp)


def extract_name(input_text):
    # Process the input text using spaCy
    doc = nlp(input_text)
    
    # Extract entities from the processed text
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Filter entities labeled as PERSON (names)
    names = [entity[0] for entity in entities if entity[1] == 'PERSON']
    
    return names


def extract_relationship(input_text):
    # Define patterns to extract person name and relationship
    patterns = [
        (r"who is (.+)'s (.+)", lambda match: (match.group(1), match.group(2))),
        (r"who is the (.+) of (.+)", lambda match: (match.group(2), match.group(1)))
    ]
    
    # Try to match input text with each pattern
    for pattern, extractor in patterns:
        match = re.match(pattern, input_text.lower())
        if match:
            return extractor(match)
    
    return None, None

# NEO4J SECTION
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "qwerty123"
driver = create_neo4j_connection(neo4j_uri, neo4j_user, neo4j_password)
create_neo4j_graph(driver)
names = get_all_node_names(driver)

# Main loop
while True:
    name_to_check = input("Hey! Ask Me: ")
    if name_to_check.lower() == 'exit':
        break
    
    name_to_check = extract_name(name_to_check)
    name_to_check = ', '.join(name_to_check)
    name_to_check = name_to_check.lower()
    
    for name in names:
        check = query_relationship(driver, name_to_check, name)
        if check != "NO":
            print(check)
            break
    else:
        print(f"Sorry, Invalid Information")

driver.close()
