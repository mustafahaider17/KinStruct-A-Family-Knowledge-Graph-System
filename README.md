# KinStruct: A Family Knowledge Graph System

KinStruct is a hybrid AI project that integrates Prolog logic, Neo4j graph databases, and spaCy NLP to allow users to query family relationships in plain English.

## 💡 Key Features

- Build a knowledge graph of family members from Prolog facts and rules
- Query relationships like "Who is Ayesha?" or "Who is Ibtisam?"
- Automatic relationship extraction using spaCy
- Graph-based reasoning via Neo4j
- Handles unknown entities gracefully

---

## 🛠️ Tech Stack

- 🧠 **Prolog (SWI-Prolog)** – for defining family relationships logically
- 🧾 **Neo4j** – to store and query relationships as a graph
- 🗣️ **spaCy** – for natural language understanding
- 🐍 **Python** – for glue logic between components

---

## 📁 Folder Structure
📦 project-root/
┣ 📄 family.pl # Prolog file with family facts and rules
┣ 📄 main.py # NLP + User interface
┣ 📄 neo4j_prolog_file.py # Graph building & querying logic
┣ 📄 requirements.txt

---

## 🧪 How It Works
- The system loads family.pl into a Prolog server.
- Converts relationships like father, mother, uncle, etc. into a Neo4j graph.
- Takes user input (like "Who is Mahnoor?") and detects names/relations using spaCy.
- Searches Neo4j for the answer and responds.
- If no match is found, it replies: "Sorry, we don’t know."
- 
