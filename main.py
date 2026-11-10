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
