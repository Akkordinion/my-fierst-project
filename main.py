import os
import chromadb
from dotenv import load_dotenv
from fastembed import TextEmbedding
from gigachat import GigaChat

load_dotenv()

client = GigaChat(
    credentials=os.getenv("GIGACHAT_CREDENTIALS"),
    scope="GIGACHAT_API_PERS",
    verify_ssl_certs=False,
    model="GigaChat-2",
)
embed_model = TextEmbedding(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
collection = chromadb.PersistentClient(path="chroma_db").get_or_create_collection(
    "python_notes", metadata={"hnsw:space": "cosine"}
)


def load_documents(folder):
    documents = []
    for name in os.listdir(folder):
        if name.endswith(".txt"):
            with open(folder + "/" + name, "r", encoding="utf-8") as f:
                documents.append({"name": name, "text": f.read()})
    return documents


def split_text(text, size=300, overlap=50):
    pieces = []
    start = 0
    while start < len(text):
        piece = text[start : start + size].strip()
        if piece:
            pieces.append(piece)
        start += size - overlap
    return pieces


def build_index(chunks):
    texts = [c["text"] for c in chunks]
    vectors = embed_model.embed(texts)
    collection.upsert(
        ids=[str(i) for i in range(len(chunks))],
        documents=texts,
        embeddings=[v.tolist() for v in vectors],
        metadatas=[{"source": c["source"]} for c in chunks],
    )


def search(question, k=3):
    vector = list(embed_model.embed([question]))[0]
    result = collection.query(query_embeddings=[vector.tolist()], n_results=k)
    return result["documents"][0], result["metadatas"][0]


def make_prompt(question, texts):
    context = "\n---\n".join(texts)
    return (
        "Ты помощник по Python. Отвечай только по тексту ниже. "
        "Если ответа в тексте нет, скажи: «В конспектах этого нет».\n\n"
        f"Текст:\n{context}\n\n"
        f"Вопрос: {question}"
    )


def ask(question):
    texts, sources = search(question)
    prompt = make_prompt(question, texts)
    try:
        response = client.chat.create(prompt)
        return response.messages[0].content[0].text, sources
    except Exception as e:
        return "Ошибка при обращении к GigaChat: " + str(e), []


if __name__ == "__main__":
    all_pieces = []
    for doc in load_documents("data"):
        for piece in split_text(doc["text"]):
            all_pieces.append({"source": doc["name"], "text": piece})
    print("Кусков:", len(all_pieces))
    build_index(all_pieces)

    answer, sources = ask("Как создать список?")
    print("Ответ:", answer)
    print("Источники:", ", ".join(set(s["source"] for s in sources)))
