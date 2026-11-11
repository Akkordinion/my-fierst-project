import os
from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")

if key is None:
    print("Ключ не найден")
    exit()

with GigaChat(
    credentials=key,
    scope="GIGACHAT_API_PERS",
    verify_ssl_certs=False,
    model="GigaChat-2",
) as client:
    response = client.chat.create("Привет! Ответь одним предложением.")
    print(response.messages[0].content[0].text)
    result = client.embeddings(
        ["Что такое список?", "Как создать список в Python?"],
        model="Embeddings-2",
    )
print(result)
