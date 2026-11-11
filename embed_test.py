from fastembed import TextEmbedding

# Часть 1: какие многоязычные модели есть
for m in TextEmbedding.list_supported_models():
    if "multilingual" in m["model"].lower():
        print(m["model"], m.get("dim"), m.get("size_in_GB"))

# Часть 2: проверка модели
model = TextEmbedding(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
texts = ["Что такое lists?", "Как создать список в Python?", "Рецепт борща"]
vectors = list(model.embed(texts))
print("Векторов:", len(vectors))
print("Чисел в каждом:", len(vectors[0]))

import math


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)


print("список и список:", cosine(vectors[0], vectors[1]))
print("список и борщ:", cosine(vectors[0], vectors[2]))
