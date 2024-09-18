# app.py
import os
import json  # Assurez-vous que cette ligne est présente
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from chatbot import get_response, initialize_rdf_graph, get_rdf_graph # Import correct

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/generate_rdf_cube', methods=['POST'])
def generate_rdf_cube():
    try:
        initialize_rdf_graph()  # Initialise le RDF graph
        graph = get_rdf_graph()  # Utilisez get_rdf_graph pour accéder au graph
        if graph is not None and len(graph) > 0:
            print(f"RDF Cube bien généré avec {len(graph)} triplets.")
            return jsonify({"message": "Cube RDF généré avec succès."})
        else:
            print("Le RDF Cube n'a pas été généré correctement ou est vide.")
            return jsonify({"message": "Erreur lors de la génération du Cube RDF."}), 500
    except Exception as e:
        print(f"Erreur dans generate_rdf_cube: {e}")
        return jsonify({"message": f"Erreur lors de la génération du Cube RDF : {e}"}), 500

@app.route('/get_response', methods=['POST'])
def chat():
    user_input = request.json.get("user_input")
    response = get_response(user_input)
    return jsonify({"response": response})

@app.route('/get_history', methods=["GET"])
def get_history():
    try:
        with open("chat_history.json", "r") as file:
            chat_history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        chat_history = []  # Initialisez une liste vide en cas d'erreur
    return jsonify({"history": chat_history})

if __name__ == "__main__":
    app.run(debug=True)
