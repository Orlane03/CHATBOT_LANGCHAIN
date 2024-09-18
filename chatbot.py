
from langchain.schema import HumanMessage
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from rdflib.plugins.sparql import prepareQuery
from rdflib import Graph
import os

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Charger la clé API depuis les variables d'environnement
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("La clé API OpenAI n'est pas définie. Assurez-vous que 'OPENAI_API_KEY' est définie dans le fichier .env.")

# Définir le modèle LLM OpenAI pour le chat avec la clé API
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)

# chatbot.py
from langchain.schema import HumanMessage


# chatbot.py
from rdflib import Graph

class RDFGraphSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RDFGraphSingleton, cls).__new__(cls)
            cls._instance.graph = Graph()  # Initialisez ici l'attribut graph
        return cls._instance

    def get_graph(self):
        if not hasattr(self, 'graph') or self.graph is None:
            self.graph = Graph()  # Réinitialisez le graph si nécessaire
        return self.graph

def initialize_rdf_graph():
    rdf_singleton = RDFGraphSingleton()
    try:
        rdf_graph = rdf_singleton.get_graph()  # Utilisez get_graph pour accéder au graph
        rdf_graph.parse(r"teaching_akg.ttl", format="turtle")
        print(f"Nombre de triplets dans le cube RDF : {len(rdf_graph)}")
    except Exception as e:
        print(f"Erreur lors du chargement du fichier RDF : {e}")
        rdf_singleton._instance = None

def get_rdf_graph():
    rdf_singleton = RDFGraphSingleton()
    return rdf_singleton.get_graph()

def get_response(user_input):
    try:
        # Vérifier si l'utilisateur pose une question liée au RDF cube
        if "sujet" in user_input.lower() or "prédicat" in user_input.lower() or "objet" in user_input.lower() or "activité" in user_input.lower():
            rdf_graph = RDFGraphSingleton().get_graph()

            if rdf_graph is not None and len(rdf_graph) > 0:
                print(f"RDF Graph contient {len(rdf_graph)} triplets.")
                sparql_query = generate_sparql_query(user_input)
                if sparql_query:
                    results = query_rdf_data(rdf_graph, sparql_query)
                    if results:
                        return format_results_as_response(results)
                    else:
                        return "Aucun résultat trouvé pour votre requête."
                else:
                    return "La requête SPARQL générée est vide ou incorrecte."
            else:
                return "Le cube RDF n'a pas encore été généré ou est vide."
        else:
            # Si ce n'est pas une question RDF, utiliser le LLM pour répondre
            print("Utilisation du LLM pour répondre à la question.")
            response = llm.invoke([HumanMessage(content=user_input)])
            return response.content

    except Exception as e:
        print(f"Erreur dans get_response: {e}")
        return "Une erreur est survenue lors du traitement de la requête."

def generate_sparql_query(user_input):
    user_input = user_input.lower()

    if "sujet" in user_input and "prédicat" not in user_input and "objet" not in user_input:
        query = """
        SELECT DISTINCT ?subject
        WHERE {
            ?subject ?predicate ?object .
        } LIMIT 10
        """
    elif "prédicat" in user_input and "sujet" not in user_input and "objet" not in user_input:
        query = """
        SELECT DISTINCT ?predicate
        WHERE {
            ?subject ?predicate ?object .
        } LIMIT 10
        """
    elif "objet" in user_input and "sujet" not in user_input and "prédicat" not in user_input:
        query = """
        SELECT DISTINCT ?object
        WHERE {
            ?subject ?predicate ?object .
        } LIMIT 10
        """
    elif "relation" in user_input:
        query = """
        SELECT ?subject ?predicate ?object
        WHERE {
            ?subject ?predicate ?object .
        } LIMIT 10
        """
    else:
        # Cas général si la question n'est pas claire
        query = """
        SELECT ?subject ?predicate ?object
        WHERE {
            ?subject ?predicate ?object .
        } LIMIT 10
        """
    
    print(f"Requête SPARQL générée : {query}")
    return query




def generate_rdf_cube():
    initialize_rdf_graph()
    if rdf_graph is not None and len(rdf_graph) > 0:
        print("Cube RDF généré avec succès.")
        return jsonify({"message": f"Cube RDF généré avec succès, contenant {len(rdf_graph)} triplets"})
    else:
        print("Le cube RDF n'a pas été généré correctement.")
        return jsonify({"message": "Erreur lors de la génération du cube RDF"}), 500

def query_rdf_data(graph, sparql_query):
    try:
        q = prepareQuery(sparql_query)
        results = graph.query(q)
        print(f"Résultats bruts de la requête : {results}")
        return results
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête SPARQL : {e}")
        return []


def save_chat(user_input, response):
    """Enregistrer la conversation dans un fichier JSON."""
    chat_entry = {
        "user": user_input,
        "bot": response
    }
    try:
        with open("chat_history.json", "r") as file:
            chat_history = json.load(file)
    except FileNotFoundError:
        chat_history = []

    chat_history.append(chat_entry)

    with open("chat_history.json", "w") as file:
        json.dump(chat_history, file, indent=4)



from rdflib import URIRef


def format_results_as_response(results):
    if len(results) == 0:
        return "Aucun résultat trouvé pour votre requête."
    
    response = "Voici les résultats :\n"
    for row in results:
        formatted_row = []
        for element in row:
            if isinstance(element, URIRef):
                label = get_label_for_uri(element)
                formatted_row.append(label if label else str(element).split('/')[-1])
            else:
                formatted_row.append(str(element))
        response += " | ".join(formatted_row) + "\n"
    return response

def get_label_for_uri(uri):
    """Essaie de récupérer un label rdfs:label pour une URI donnée"""
    try:
        query = f"""
        SELECT ?label WHERE {{
            <{uri}> rdfs:label ?label .
        }} LIMIT 1
        """
        rdf_graph = RDFGraphSingleton().get_graph()
        results = rdf_graph.query(query)
        for row in results:
            return str(row.label)
    except Exception as e:
        print(f"Erreur lors de la récupération du label pour {uri}: {e}")
        return None
