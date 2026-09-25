from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


KNOWLEDGE_DIR = Path("data/knowledge")


class KnowledgeBase:

    def __init__(self):
        self.embedder = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path=".chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name="support_knowledge"
        )

        self._load_documents()

    def _load_documents(self):

        documents = []
        ids = []
        metadatas = []

        for path in KNOWLEDGE_DIR.glob("*.md"):

            text = path.read_text(
                encoding="utf-8"
            )

            documents.append(text)
            ids.append(path.stem)
            metadatas.append(
                {"source": path.name}
            )

        if not documents:
            return

        embeddings = self.embedder.encode(
            documents
        ).tolist()

        existing = self.collection.get()

        existing_ids = set(existing["ids"])

        new_documents = []
        new_ids = []
        new_metadatas = []
        new_embeddings = []

        for document, doc_id, metadata, embedding in zip(
            documents,
            ids,
            metadatas,
            embeddings,
        ):

            if doc_id not in existing_ids:

                new_documents.append(document)
                new_ids.append(doc_id)
                new_metadatas.append(metadata)
                new_embeddings.append(embedding)

        if new_documents:

            self.collection.add(
                documents=new_documents,
                ids=new_ids,
                metadatas=new_metadatas,
                embeddings=new_embeddings,
            )

    def search(
        self,
        query: str,
        top_k: int = 3,
    ):

        embedding = self.embedder.encode(
            [query]
        ).tolist()

        result = self.collection.query(
            query_embeddings=embedding,
            n_results=top_k,
        )

        documents = result["documents"][0]
        metadatas = result["metadatas"][0]

        return list(
            zip(documents, metadatas)
        )