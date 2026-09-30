from src.loaders.text_loader import load_directory


documents = load_directory("data/raw")

for document in documents:
    print("SOURCE:", document["source"])
    print("TEXT:")
    print(document["text"])
    print("--------------------")