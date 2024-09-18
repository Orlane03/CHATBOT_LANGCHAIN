# Chatbot avec Langchain et RDF Cube

## Description

Cette application est un **chatbot intelligent** capable de répondre à des questions générales en utilisant un modèle de langage naturel (LLM) et des questions spécifiques basées sur des données structurées RDF. Le chatbot intègre **OpenAI GPT-3.5-turbo** via **Langchain** pour le traitement des requêtes générales, et utilise **RDF Cube** pour fournir des réponses précises à partir de données RDF.

## Fonctionnalités

- **Dialogue hybride :** Utilisation du modèle de langage GPT-3.5 pour les questions générales et des données RDF pour des requêtes spécifiques.

- **Génération de cubes RDF :** Intègre un graphe RDF pour répondre aux requêtes structurées via des requêtes SPARQL.

- **Interface Web :** Simple et intuitive, développée avec Flask.

- **Sauvegarde de l'historique :** Les conversations sont enregistrées dans un fichier JSON pour une consultation ultérieure.

## Structure du projet

```bash
.
├── chatbot-env/          # Environnement virtuel Python
├── env/                  # Fichiers d'environnement (variables .env)
├── static/               # Dossier pour les fichiers statiques (CSS, JS, images)
├── templates/
│   └── index.html        # Page principale de l'interface utilisateur
├── app.py                # Serveur Flask pour gérer les requêtes utilisateur
├── chatbot.py            # Logique principale du chatbot (LLM et RDF)
├── main.py               # Interface en ligne de commande pour le chatbot
├── chat_history.json      # Fichier d'historique des conversations
├── requirements.txt      # Dépendances du projet
├── teaching_akg.ttl      # Fichier de données RDF en format Turtle
└── README.md             # Fichier d'explication du projet
```

# Prérequis

1. **Python 3.8+** doit être installé sur votre machine.
2. Créez un environnement virtuel pour isoler les dépendances :

```bash
    python3 -m venv chatbot-env
    source chatbot-env/bin/activate  # Sur Windows: chatbot-env\Scripts\activate
```

3. Installez les dépendances à partir du fichier `requirements.txt` :

```bash
    pip install -r requirements.txt
    pip install rdflib
```

4. Créez un fichier `.env` pour ajouter votre clé API OpenAI :

```bash
    touch .env
```
    Ajoutez la ligne suivante dans ce fichier `.env` :
```bash
    OPENAI_API_KEY=your_openai_api_key
```

## Exécution de l'application

1. **Interface Web**
Pour démarrer l'interface Web :
```bash
    python app.py
```
L'application sera disponible à l'adresse `http://127.0.0.1:5000/`.

2. **Interface en Ligne de Commande (CLI)**
Pour exécuter le chatbot dans une interface en ligne de commande :
```bash
    python main.py
```

## Utilisation

1. **Génération du Cube RDF :** Depuis l'interface web, cliquez sur le bouton Générer le cube RDF. Cela initialise le graphe RDF en chargeant les données du fichier teaching_akg.ttl.

2. **Poser des questions :** Vous pouvez poser des questions générales (gérées par GPT-3.5) ou des questions spécifiques liées aux données RDF (gérées via des requêtes SPARQL).

3. **Historique des conversations :** L'historique des conversations est disponible dans l'interface ou peut être consulté dans le fichier chat_history.json.

## Technologies utilisées

- **Flask :** Framework web léger pour gérer les requêtes serveur.
- **Langchain :** Framework pour la création de chaînes NLP, utilisé pour intégrer GPT-3.5-turbo.
- **RDFLib :** Utilisé pour manipuler et interroger les graphes RDF.
- **OpenAI GPT-3.5-turbo :** Modèle de langage utilisé pour répondre aux questions générales.

## Auteur

Développé par :

        - MASOBELE MVITA Charly
        - SONKENG TSAFACK Orlane
        - ISSA SORO Fiti
        - NZAZI NGABILA Boaz

## Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser et de le modifier.

## Vidéo de démonstration


