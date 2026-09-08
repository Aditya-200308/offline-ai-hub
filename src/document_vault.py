"""
Local Document Vault (100% On-Device Private RAG)
Parses local files and performs 100% on-device semantic retrieval with zero external calls.
"""

import io
import re
import math
from typing import List, Dict, Tuple


class LocalDocumentVault:
    """100% on-device document extraction and lightweight vector retrieval engine."""

    def __init__(self):
        self.documents: List[Dict] = []
        self.chunks: List[Dict] = []
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}

    def ingest_file(self, file_name: str, file_bytes: bytes) -> Dict:
        """Extracts text from uploaded file bytes completely in-memory."""
        text = ""
        file_ext = file_name.split(".")[-1].lower() if "." in file_name else "txt"

        if file_ext == "pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                pages = [page.extract_text() or "" for page in reader.pages]
                text = "\n\n".join(pages)
            except Exception as e:
                text = f"[PDF Extraction Error: {str(e)}]"

        elif file_ext in ["docx", "doc"]:
            try:
                import docx
                doc = docx.Document(io.BytesIO(file_bytes))
                text = "\n".join([p.text for p in doc.paragraphs if p.text])
            except Exception as e:
                text = f"[DOCX Extraction Error: {str(e)}]"

        else:
            # Fallback to UTF-8 text (.txt, .py, .csv, .json, .md, .env)
            try:
                text = file_bytes.decode("utf-8", errors="replace")
            except Exception:
                text = str(file_bytes)

        # Chunk the document
        new_chunks = self._chunk_text(text, file_name, max_chars=600, overlap=100)
        self.chunks.extend(new_chunks)
        self.documents.append({
            "name": file_name,
            "char_count": len(text),
            "chunk_count": len(new_chunks),
            "size_kb": round(len(file_bytes) / 1024, 2)
        })

        # Re-index vocabulary & IDF
        self._build_index()

        return {
            "name": file_name,
            "chunks_created": len(new_chunks),
            "total_chars": len(text)
        }

    def _chunk_text(self, text: str, source_name: str, max_chars: int = 600, overlap: int = 100) -> List[Dict]:
        """Splits text preserving sentence boundaries with character overlap."""
        sentences = re.split(r'(?<=[.!?\n])\s+', text)
        chunks = []
        current_chunk = []
        current_len = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if current_len + len(sentence) > max_chars and current_chunk:
                chunk_str = " ".join(current_chunk)
                chunks.append({
                    "source": source_name,
                    "chunk_id": len(chunks) + 1,
                    "text": chunk_str
                })
                # Maintain overlap from trailing sentence
                current_chunk = [current_chunk[-1]] if len(current_chunk) > 1 else []
                current_len = sum(len(s) for s in current_chunk)

            current_chunk.append(sentence)
            current_len += len(sentence)

        if current_chunk:
            chunks.append({
                "source": source_name,
                "chunk_id": len(chunks) + 1,
                "text": " ".join(current_chunk)
            })

        return chunks

    def _tokenize(self, text: str) -> List[str]:
        """Simple, fast regex tokenizer."""
        return re.findall(r'\b[a-zA-Z0-9_]{2,}\b', text.lower())

    def _build_index(self):
        """Builds in-memory TF-IDF index across all chunks."""
        doc_freq = {}
        total_docs = len(self.chunks)

        for chunk in self.chunks:
            tokens = set(self._tokenize(chunk["text"]))
            for t in tokens:
                doc_freq[t] = doc_freq.get(t, 0) + 1

        self.idf = {
            token: math.log((total_docs + 1) / (df + 1)) + 1.0
            for token, df in doc_freq.items()
        }

    def search(self, query: str, top_k: int = 3) -> List[Tuple[Dict, float]]:
        """Computes TF-IDF cosine similarity scores entirely in local memory."""
        if not self.chunks:
            return []

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return [(c, 0.0) for c in self.chunks[:top_k]]

        query_vec = {}
        for t in query_tokens:
            query_vec[t] = query_vec.get(t, 0) + 1
        
        # Apply IDF to query
        for t in query_vec:
            query_vec[t] *= self.idf.get(t, 1.0)

        query_norm = math.sqrt(sum(v ** 2 for v in query_vec.values())) or 1.0

        scores = []
        for chunk in self.chunks:
            chunk_tokens = self._tokenize(chunk["text"])
            chunk_tf = {}
            for t in chunk_tokens:
                chunk_tf[t] = chunk_tf.get(t, 0) + 1

            # Cosine similarity dot product
            dot_product = 0.0
            chunk_norm_sq = 0.0
            for t, tf in chunk_tf.items():
                w = tf * self.idf.get(t, 1.0)
                chunk_norm_sq += w ** 2
                if t in query_vec:
                    dot_product += query_vec[t] * w

            chunk_norm = math.sqrt(chunk_norm_sq) or 1.0
            similarity = dot_product / (query_norm * chunk_norm)
            scores.append((chunk, round(similarity, 4)))

        # Sort descending by similarity
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def clear(self):
        """Flushes in-memory documents and vector indices."""
        self.documents = []
        self.chunks = []
        self.vocabulary = {}
        self.idf = {}
