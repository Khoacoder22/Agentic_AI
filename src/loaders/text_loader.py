from pathlib import Path

# data/raw -> loaders -> documents

def load_text_file(file_path: str) -> str:
    path = Path(file_path)

    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def load_directory(directory: str):
    documents = []

    path = Path(directory)

    for file_path in path.glob("*.txt"):
        text = load_text_file(str(file_path))

        documents.append({
            "source": file_path.name,
            "text": text
        })

    return documents