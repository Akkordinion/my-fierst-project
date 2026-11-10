import os

folder = "data"

documents = []

for name in os.listdir(folder):
    path = folder + "/" + name
    f = open(path, "r", encoding="utf-8")
    text = f.read()
    f.close()
    documents.append({"name": name, "text": text})
print("Прочитано файлов:", len(documents))


def split_text(text, size, overlap):
    step = size - overlap
    windows = []
    start = 0
    while start < len(text):
        piece = text[start : start + size]
        windows.append(piece)
        start += step
    return windows


all_pieces = []  # общая коробка

for doc in documents:  # берём документы по одному
    pieces = split_text(doc["text"], 300, 50)  # режем его числа
    for piece in pieces:  # берём кусочки по одному
        all_pieces.append({"source": doc["name"], "text": piece})

print("Всего кусочков:", len(all_pieces))
for p in all_pieces:
    print(p)
