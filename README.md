# Guess the Song Game Bot 🎵

An interactive Tamil music trivia game powered by Generative AI. This project implements a **Retrieval-Augmented Generation (RAG)** pipeline to provide accurate, context-aware song trivia while maintaining strict game logic via a deterministic state machine.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anublossom/-Guess_the_song_game_bot/blob/main/Guess_the_song/app.py)

## 🎯 Project Overview
The **Guess the Song Game Bot** is an NLP-driven application designed to challenge users with A.R. Rahman’s discography[cite: 1]. It solves the "hallucination problem" typical in LLMs by using a hybrid architecture: the AI handles creative dialogue, while a deterministic Python layer ensures game mechanics and lyric data remain 100% accurate[cite: 1].

## 🏗️ How this project functions as a RAG Pipeline
* **Retrieval Layer:** ChromaDB is used as a vector store to house lyric data[cite: 1]. Instead of relying on an LLM's limited memory, the system queries this database to fetch the exact, authentic next line of a song, preventing hallucinations[cite: 1].
* **Augmentation Layer:** The "Command Intercept Layer" acts as deterministic augmentation[cite: 1]. Before sending data to the LLM, the system injects specific, accurate lyric lines retrieved from the database into the system prompt[cite: 1].
* **Generation Layer:** The Llama-3.1-8b-instant LLM acts as the generator[cite: 1]. It receives the augmented context (the retrieved lyric line) and generates a creative, witty response for the user while remaining bound by strict "Negative Constraints" defined in the prompt[cite: 1].

## ⚙️ Technical Architecture
### 1. Data Engineering & Semantic Search
* **Data Engineering:** Harvests lyrics via `LRCLIB API` and processes them using a custom `Regex` pipeline to normalize "Tanglish" (Romanized Tamil) by stripping speaker tags and noise[cite: 1].
* **Vector Database:** Uses **ChromaDB** for local persistent storage, mapping lyric context to metadata (Song, Movie, Composer)[cite: 1].
* **Semantic Search:** Employs the `intfloat/multilingual-e5-base` model to create dense mathematical embeddings, allowing the system to understand the "vibe" and semantic meaning of lyrics[cite: 1].

### 2. LLM Brain & Orchestration
* **LLM Interface:** Leverages `llama-3.1-8b-instant` (via Groq Cloud API) for natural language understanding and creative clue generation[cite: 1].
* **Deterministic Orchestration:** Managed by a hybrid state-machine flow (modeled after `LangGraph`)[cite: 1]. A central Python loop intercepts user commands (e.g., "skip", "next line"), preventing the AI from hallucinating or breaking game rules[cite: 1].
* **Prompt Engineering:** Uses instruction-based system prompting with negative constraints to force the AI into a witty trivia host persona while strictly forbidding the leak of song metadata[cite: 1].

## 🛠️ Exhaustive Technical Stack

| Category | Component | Purpose |
| :--- | :--- | :--- |
| **Languages** | Python | The primary programming language used for the entire application logic[cite: 1]. |
| **Data Scraping** | Cloudscraper | Used to bypass Cloudflare firewalls during API requests[cite: 1]. |
| **Data APIs** | LRCLIB API | The external source used to harvest song lyrics[cite: 1]. |
| **Data Processing** | Pandas | Used for data manipulation, cleaning, and creating the CSV database[cite: 1]. |
| **Data Processing** | Regex (re) | Used for text cleaning, stripping non-Latin scripts, and removing speaker tags[cite: 1]. |
| **LLM / AI Model** | Llama-3.1-8b-instant | The LLM brain used via the Groq API to generate clues and chat with the user[cite: 1]. |
| **LLM Provider** | Groq Cloud API | The high-speed inference engine hosting the LLM[cite: 1]. |
| **Embeddings** | intfloat/multilingual-e5-base | The model used to convert lyrics into mathematical vector coordinates[cite: 1]. |
| **Vector Search** | ChromaDB | The persistent local storage used as a vector database for song context retrieval[cite: 1]. |
| **Orchestration** | LangGraph | Used for managing the state-machine flow of the game nodes and edges[cite: 1]. |
| **Orchestration** | LangChain | The framework used to interface with the Groq LLM and manage prompts[cite: 1]. |
| **Architecture** | Deterministic State-Machine | A rigid logic loop that controls game rules and prevents AI hallucinations[cite: 1]. |
| **Concepts** | Vector Embeddings | Mathematical arrays capturing the semantic meaning of lyric text[cite: 1]. |
| **Concepts** | Prompt Engineering | The technique of using system instructions to enforce negative constraints and persona[cite: 1]. |
| **Concepts** | Few-Shot Prompting | Providing contextual examples within prompts to guide AI output[cite: 1]. |

## 🚀 How to Run
1. **Google Colab:** Click the "Open in Colab" badge above to run directly in the cloud[cite: 1].
2. **Local Execution:**
   ```bash
   git clone [https://github.com/anublossom/-Guess_the_song_game_bot.git](https://github.com/anublossom/-Guess_the_song_game_bot.git)
   python app.py
