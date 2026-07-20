import os
import random
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq

# Setup Groq API Key via environment variable or hardcoded string fallback
MY_FREE_KEY = os.getenv("GROQ_API_KEY", "YOUR_API_KEY")

# Connect back to the local vector directory pool
chroma_client = chromadb.PersistentClient(path="rahman_vector_db")
collection = chroma_client.get_collection(name="rahman_tamil_songs")
embedding_model = SentenceTransformer("intfloat/multilingual-e5-base")

# Initialize LLM with a friendly conversational temperature profile
host_llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=MY_FREE_KEY, temperature=0.6)

def play_conversational_game():
    all_records = collection.get()
    
    if not all_records or len(all_records['documents']) == 0:
        print("❌ Error: ChromaDB is empty. Please run your data ingestion indexing script first!")
        return

    # Select a random song out of our dataset rows
    idx = random.randint(0, len(all_records['documents'])-1)
    hidden_lyrics = all_records['documents'][idx]
    correct_song = all_records['metadatas'][idx]['title']
    correct_movie = all_records['metadatas'][idx]['movie']

    # Clean up the lyrics list array structure line-by-line
    full_lines_pool = [l.strip() for l in hidden_lyrics.split('\n') if len(l.strip().split()) >= 3]

    # Game state variables
    current_line_index = 0
    chat_history = []
    attempts = 0

    if not full_lines_pool:
        full_lines_pool = ["chinna chinna aasai", "siragadikki aasai", "muthu muthu aasai"]

    iconic_line = full_lines_pool[current_line_index]

    print("\n🎙️ [Game Host]: Hello! I am your interactive A.R. Rahman trivia host. Let's have some fun.")
    print(f"🎵 [Lyric Clue Line]: \"{iconic_line}\"")
    print("💬 (Commands: 'next line', 'give answer', 'skip', or chat freely!)")

    while True:
        user_input = input("\n#️⃣ You: ").strip()
        cleanup_command = user_input.lower().strip()

        # --- ORCHESTRATOR INTERCEPT 1: SKIP CONTROL ---
        if any(cmd in cleanup_command for cmd in ["skip", "change", "next song", "other song"]):
            print("\n🔄 [System]: Spinning up a brand new track card...")
            return play_conversational_game()

        # --- ORCHESTRATOR INTERCEPT 2: REAL NEXT LINE FETCHING (TYPO PROTECTED) ---
        if any(cmd in cleanup_command for cmd in ["next line", "give next line", "more lyrics", "nextline", "nexxt"]):
            current_line_index += 1
            if current_line_index < len(full_lines_pool):
                next_lyrics = full_lines_pool[current_line_index]
                print(f"\n🎙️ [Game Host]: You want more text details? Say no more! Here is the actual next line from the composition:")
                print(f"🎵 \"{next_lyrics}\"")
                chat_history.append(f"System: Revealed next line: {next_lyrics}")
                continue
            else:
                print("\n🎙️ [Game Host]: Whoops! That is the end of the lyric file sheet. Time to guess!")
                continue

        # --- ORCHESTRATOR INTERCEPT 3: FORCE REVEAL ANSWER (TYPO PROTECTED) ---
        if any(cmd in cleanup_command for cmd in ["give answer", "reveal answer", "i give up", "tell me", "reveal", "answer"]):
            print(f"\n🎙️ [Game Host]: Alright, throwing in the towel? No shame in that! The hidden masterpiece was:")
            print(f"🏆 Song: **{correct_song}** | Movie: **{correct_movie}**")
            print("=======================================================")
            return play_conversational_game()

        # Standard conversational fallback via Llama processing layer
        master_system_prompt = f"""
        You are a fun game host for an A.R. Rahman music trivia game.
        Secret Answer: Song '{correct_song}' from Movie '{correct_movie}'.
        Initial clue words shown: "{iconic_line}"
        Current incorrect guess count: {attempts}

        CRUCIAL INSTRUCTIONS:
        1. Never output the exact song '{correct_song}' or movie '{correct_movie}' strings unless the player guesses it right.
        2. If the user talks to you or argues about something (e.g., 'this is a Hindi song'), chat back naturally like a human music nerd.
        3. If they name the correct movie or song, respond with high energy and put 'GAME_WON_MOVE_ON' at the absolute end of your response.

        Past Chat Flow Context:
        {chat_history[-4:]}

        User Input: "{user_input}"
        Your Chat Response:"""

        response = host_llm.invoke(master_system_prompt)
        reply_text = response.content.strip()

        if "GAME_WON_MOVE_ON" in reply_text:
            clean_reply = reply_text.replace("GAME_WON_MOVE_ON", "").strip()
            print(f"\n🎙️ [Game Host]: {clean_reply}")
            print("\n=======================================================")
            return play_conversational_game()

        print(f"\n🎙️ [Game Host]: {reply_text}")
        chat_history.append(f"User: {user_input}\nHost: {reply_text}")
        attempts += 1

if __name__ == "__main__":
    play_conversational_game()
