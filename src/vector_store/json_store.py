import json
from pathlib import Path


def save_vectors( documents, file_path="data/processed/vector_store.json"):
    path = Path(file_path)

    path.parent.mkdir( parents=True, exist_ok=True )

    with open( path, "w", encoding="utf-8"
    ) as file:
        json.dump(
            documents,
            file,
            ensure_ascii=False
        )


def load_vectors(
    file_path="data/processed/vector_store.json"
):
    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)