
from neo4j import GraphDatabase
from swiplserver import PrologMQI

def create_neo4j_connection(uri, user, password):
    return GraphDatabase.driver(uri, auth=(user, password))

# Function to create nodes and relationships in Neo4j
def create_neo4j_graph(driver):
    # Create a connection to Prolog server
    prolog_thread = PrologMQI().create_thread()

    # Consult the Prolog file
    prolog_thread.query(r"consult('C:\\Users\\Salman Joyia\\OneDrive\\Desktop\\chatbot\\family.pl')")


    with driver.session() as session:
        # Define a dictionary to map Prolog predicates to Neo4j relationship types
        relationship_mapping = {
            "father": "FATHER_OF",
            "mother": "MOTHER_OF",
            "grandfather": "GRANDFATHER_OF",
            "grandmother": "GRANDMOTHER_OF",
            "uncle": "UNCLE_OF",
            "aunt": "AUNT_OF",
            "brother": "BROTHER_OF",
            "sister": "SISTER_OF"
        }

        # Iterate over each rule and query Prolog for relationships
        for prolog_rule, neo4j_relationship in relationship_mapping.items():
            # Query Prolog for relationships based on the rule
            for fact in prolog_thread.query(f"{prolog_rule}(X, Y)"):
                # Create nodes and relationships in Neo4j
                session.run(f"MERGE (person1:Person {{name: $person1_name}}) "
                            f"MERGE (person2:Person {{name: $person2_name}}) "
                            f"MERGE (person1)-[:{neo4j_relationship}]->(person2)",
                            person1_name=fact["X"], person2_name=fact["Y"])
    del prolog_thread

def query_relationship(driver, person1_name, person2_name):
    with driver.session() as session:
        for relationship_type in ["FATHER_OF", "MOTHER_OF", "GRANDFATHER_OF", "GRANDMOTHER_OF", "UNCLE_OF", "AUNT_OF", "BROTHER_OF", "SISTER_OF"]:
            query = f"MATCH (p1:Person)-[r:{relationship_type}]->(p2:Person) WHERE p1.name = $person1_name AND p2.name = $person2_name RETURN type(r) AS relationship LIMIT 1"
            result = session.run(query, person1_name=person1_name, person2_name=person2_name)
            record = result.single()
            if record:
                if relationship_type == "FATHER_OF":
                    return(f"{person1_name} is father of {person2_name}")
                elif relationship_type == "MOTHER_OF":
                    return(f"{person1_name} is mother of {person2_name}")
                elif relationship_type == "GRANDFATHER_OF":
                    return(f"{person1_name} is grandfather of {person2_name}")
                elif relationship_type == "GRANDMOTHER_OF":
                    return(f"{person1_name} is grandmother of {person2_name}")
                elif relationship_type == "UNCLE_OF":
                    return(f"{person1_name} is uncle of {person2_name}")
                elif relationship_type == "AUNT_OF":
                    return(f"{person1_name} is aunt of {person2_name}")
                elif relationship_type == "BROTHER_OF":
                    return(f"{person1_name} is brother of {person2_name}")
                elif relationship_type == "SISTER_OF":
                    return(f"{person1_name} is sister of {person2_name}")
                break
        else:
            return("NO")

def get_all_node_names(driver):
    node_names = []
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN n.name AS name")
        for record in result:
            node_names.append(record["name"])
    return node_names
