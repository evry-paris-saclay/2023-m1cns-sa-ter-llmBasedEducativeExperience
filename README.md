# 2023-m1cns-sa-ter-llmBasedEducativeExperience
## Contexte
Ce projet intègre des modèles de langage avancés (LLM) pour soutenir les enseignants et enrichir l'expérience des étudiants. L'assistant développé permet d'analyser des contenus éducatifs et de générer des interactions basées sur ces analyses, facilitant ainsi la création de matériel pédagogique interactif.

## Objectifs
- **Support enseignant** : Fournir des analyses et des suggestions de contenu en temps réel pour aider les enseignants à préparer et à enrichir leurs cours.
- **Engagement des étudiants** : Offrir aux étudiants des possibilités d'interaction avec le matériel de cours grâce à des fonctionnalités générant des quiz, des questions, et des exemples à partir des textes.

## Installation
Pour mettre en place et exécuter ce projet, suivez les instructions ci-dessous :

### Prérequis
- Python 3.x doit être installé sur votre machine. Téléchargez-le et installez-le depuis [python.org](https://www.python.org/downloads/).
- Téléchargez et installez `Ollama` depuis [ollama.com](https://ollama.com/) pour permettre l'analyse avancée du langage.

### Dépendances
Les dépendances nécessaires sont listées dans le fichier `src/requirements.txt` du projet.
## Configuration
Créez un fichier `.env` à la racine de votre projet et ajoutez-y la clé API nécessaire pour le modèle LLM, dans notre cas on utilise une API de Groq que vous pouvez créer un compte et avoir accés a une API directement sur [GroqCloud.com](https://console.groq.com/)
```plaintext
GROQ_API_KEY="votre_clé_api"
```
## Exécution

Pour exécuter l'application, suivez ces étapes :

1. Compilez le fichier `app.py`.
2. Une fois compilé avec succès, utilisez la commande suivante dans votre terminal pour exécuter l'application :
   ```bash
   chainlit run app.py
## Utilisation

Une fois que le script est démarré, l'interface de l'assistant vous guidera à travers les étapes suivantes :
![Exemple d'utilisation](C:/Users/DJELLOUDI/Pictures/demo.png)
- Téléchargez un fichier PDF contenant le contenu éducatif.
- L'assistant extrait automatiquement le texte du PDF téléchargé.
- Les utilisateurs peuvent interagir avec l'assistant en posant des questions directes ou en utilisant des boutons pour générer des quiz, des questions et des exemples basés sur le texte extrait.

## Fonctionnalités

- **Extraction et analyse de texte** : L'assistant est capable de lire et d'interpréter le contenu des documents PDF.
- **Génération de contenu interactif** : Il peut créer des questions, des quiz et des exemples basés sur le texte extrait pour enrichir l'expérience d'apprentissage.
- **Interaction en temps réel** : L'assistant répond aux requêtes des utilisateurs de manière interactive, améliorant ainsi l'expérience d'apprentissage.
## Conclusion

`llmBasedEducativeExperience` exploite les technologies de traitement du langage naturel pour offrir un outil d'assistance et d'engagement, améliorant ainsi l'expérience en classe. Conçu pour soutenir les enseignants dans la gestion de leurs cours et encourager l'interaction des étudiants, cet outil rend les interactions en classe plus dynamiques et enrichissantes.


