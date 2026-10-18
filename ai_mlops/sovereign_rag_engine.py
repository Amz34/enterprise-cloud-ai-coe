"""Sovereign In-Kingdom RAG Engine for Engineering Standards (Aramco/SABIC Aligned)."""
import math
import re

class SovereignRAGMatcher:
    """Deterministic, air-gapped vector similarity simulator for technical specifications."""
    def __init__(self):
        self.documents = [
            {
                "id": "ARAMCO-SAES-L-105",
                "title": "Piping System Design & Material Specifications",
                "content": "Piping design temperature and pressure ratings shall comply with ASME B31.3. Stainless steel 316L required for high-corrosion zones."
            },
            {
                "id": "SABIC-ENG-STD-402",
                "title": "Industrial Rotating Equipment Vibration Standards",
                "content": "Centrifugal pumps and compressors vibration RMS limits shall not exceed 0.050 mm/s during steady-state operation."
            },
            {
                "id": "NCA-ECC-1-2018",
                "title": "Essential Cybersecurity Controls for Critical Infrastructure",
                "content": "All industrial control networks must implement strict zone segregation, multi-factor authentication, and air-gapped audit logging."
            }
        ]

    def _tokenize(self, text: str):
        return set(re.findall(r'\b[a-zA-Z0-9_-]+\b', text.lower()))

    def query(self, search_text: str, top_k: int = 2):
        query_tokens = self._tokenize(search_text)
        results = []
        for doc in self.documents:
            doc_tokens = self._tokenize(doc["title"] + " " + doc["content"])
            intersection = query_tokens.intersection(doc_tokens)
            score = len(intersection) / (math.sqrt(len(query_tokens) * len(doc_tokens)) + 1e-5)
            if score > 0:
                results.append({"doc_id": doc["id"], "score": round(score, 4), "title": doc["title"], "content": doc["content"]})
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

if __name__ == "__main__":
    rag = SovereignRAGMatcher()
    q = "vibration limits for rotating compressors"
    print(f"Query: '{q}'")
    matches = rag.query(q)
    for m in matches:
        print(f"Matched [{m['doc_id']}] (Score: {m['score']}): {m['title']}")
