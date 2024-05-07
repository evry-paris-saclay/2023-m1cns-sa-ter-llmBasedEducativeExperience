import PyPDF2
import chainlit as cl
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import random
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Initialiser le modèle de chat basé sur l'API Groq avec une clé d'API et des paramètres spécifiques
groq_api_key = os.environ['GROQ_API_KEY']
llm_groq = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="mixtral-8x7b-32768",
    temperature=0.2
)

# Définir une fonction qui s'exécute lorsque le chat démarre
@cl.on_chat_start
async def on_chat_start():
    files = None
    # Boucle pour demander et recevoir un fichier PDF de l'utilisateur
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a pdf file to begin!",
            accept=["application/pdf"],
            max_size_mb=100,
            timeout=180
        ).send()
    file = files[0]

    # Lire et extraire le texte du fichier PDF
    pdf = PyPDF2.PdfReader(file.path)
    pdf_text = ""
    for page in pdf.pages:
        pdf_text += page.extract_text()

    # Stocker le texte complet du PDF dans la session de l'utilisateur
    cl.user_session.set("full_pdf_text", pdf_text)

    # Découper le texte pour le traitement et préparer les métadonnées pour la recherche de documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=50)
    texts = text_splitter.split_text(pdf_text)
    metadatas = [{"source": f"{i}-pl"} for i in range(len(texts))]

    # Charger les embeddings et initialiser la recherche de documents
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    docsearch = await cl.make_async(Chroma.from_texts)(
        texts, embeddings, metadatas=metadatas
    )

    # Initialiser l'historique des messages et la mémoire de conversation
    message_history = ChatMessageHistory()
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )

    # Configurer une chaîne de conversation pour la recherche et la génération de réponses
    chain = ConversationalRetrievalChain.from_llm(
        llm_groq,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )

    # Définir des actions et envoyer un message pour démarrer l'interaction
    actions = [
        cl.Action(name="generate_examples", label="Generate Examples", value="ge"),
        cl.Action(name="generate_quiz", label="Generate Quiz", value="gq"),
        cl.Action(name="generate_questions", label="Generate Questions", value="gqe")
    ]
    await cl.Message(content=f"Processing `{file.name}` done. You can now ask questions or use the buttons below!", actions=actions).send()
    cl.user_session.set("chain", chain)

# Définir une fonction pour traiter les messages reçus durant le chat
@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")
    if message.content.lower() in ["ge", "gq", "gqe"]:
        return  # Ignorer le traitement si l'utilisateur clique sur une action
    
    # Générer une réponse en utilisant la chaîne de conversation configurée
    res = await chain.ainvoke(message.content)
    answer = res["answer"]

    # Ajouter des boutons avec chaque réponse pour un accès facile
    actions = [
        cl.Action(name="generate_examples", label="Generate Examples", value="ge"),
        cl.Action(name="generate_quiz", label="Generate Quiz", value="gq"),
        cl.Action(name="generate_questions", label="Generate Questions", value="gqe")
    ]
    await cl.Message(content=answer, actions=actions).send()

# Définition des fonctions pour gérer les actions spécifiques de l'utilisateur
# Chaque fonction génère du contenu basé sur le texte du PDF stocké
@cl.action_callback("generate_examples")
async def handle_generate_examples(action):
    full_text = cl.user_session.get("full_pdf_text", "")
    response_text = generate_examples(full_text)
    await cl.Message(content=response_text).send()

@cl.action_callback("generate_quiz")
async def handle_generate_quiz(action):
    full_text = cl.user_session.get("full_pdf_text", "")
    response_text = generate_quiz_questions(full_text)
    await cl.Message(content=response_text).send()

@cl.action_callback("generate_questions")
async def handle_generate_questions(action):
    full_text = cl.user_session.get("full_pdf_text", "")
    response_text = generate_questions(full_text)
    await cl.Message(content=response_text).send()

# Fonctions pour générer des exemples, des quiz et des questions
# Utilisent une graine aléatoire pour encourager la variété
def generate_examples(text):
    random_seed = random.randint(1, 100)
    prompt = (f"Using seed {random_seed}, generate exactly 5 creative examples that clearly illustrate "
              f"different key concepts from the following text. Include examples that are analogies, real-world applications, "
              f"historical parallels, and hypothetical scenarios to enrich understanding:\n\n{text}")
    result = llm_groq.invoke(prompt)
    return result.content if hasattr(result, 'content') else "Failed to generate creative and varied examples."

def generate_quiz_questions(text):
    random_seed = random.randint(1, 100)
    prompt = (f"Using seed {random_seed}, generate exactly five quiz questions based on the text below. "
              f"Each question should include one correct answer, three plausible but incorrect alternatives, "
              f"and provide a detailed explanation for why the correct answer is right, emphasizing the relevance "
              f"and implications of the answer. Ensure the questions cover a range of topics such as factual details, "
              f"analytical insights, application-based scenarios, and theoretical understanding:\n\n{text}")
    result = llm_groq.invoke(prompt)
    return result.content if hasattr(result, 'content') else "Failed to generate a set of five quiz questions with detailed explanations."

def generate_questions(text):
    themes = ["Factual Details", "Interpretative Insights", "Critical Evaluations"]
    random_theme = random.choice(themes)
    random_seed = random.randint(1, 100)
    prompt = (f"Using seed {random_seed}, please generate exactly 5 unique questions focusing on '{random_theme}'. "
              f"Explore new aspects not previously covered and ensure that questions span different facets of the theme:\n\n{text}")
    result = llm_groq.invoke(prompt)
    return result.content if hasattr(result, 'content') else "Failed to generate diverse and specific questions."