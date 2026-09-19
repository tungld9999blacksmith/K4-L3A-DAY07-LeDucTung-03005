from __future__ import annotations

import math
import re


class FixedSizeChunker:
    """
    Split text into fixed-size chunks with optional overlap.

    Rules:
        - Each chunk is at most chunk_size characters long.
        - Consecutive chunks share overlap characters.
        - The last chunk contains whatever remains.
        - If text is shorter than chunk_size, return [text].
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        if len(text) <= self.chunk_size:
            return [text]

        step = self.chunk_size - self.overlap
        chunks: list[str] = []
        for start in range(0, len(text), step):
            chunk = text[start : start + self.chunk_size]
            chunks.append(chunk)
            if start + self.chunk_size >= len(text):
                break
        return chunks


class SentenceChunker:
    """
    Split text into chunks of at most max_sentences_per_chunk sentences.

    Sentence detection: split on ". ", "! ", "? " or ".\n".
    Strip extra whitespace from each chunk.
    """

    def __init__(self, max_sentences_per_chunk: int = 3) -> None:
        self.max_sentences_per_chunk = max(1, max_sentences_per_chunk)

    def chunk(self, text: str) -> list[str]:
        # TODO: split into sentences, group into chunks
        import re
        if not text:
            return []
        # split text using splitted characters as . , ! ? or .\n
        sentences = re.split(r'(?<!\d)[.!?](?=\s|$)', text.strip())
        sentences = [sentence for sentence in sentences if sentence]

        chunks: list[str] = []
        for index in range(0, len(sentences), self.max_sentences_per_chunk):
            chunks.append(" ".join(sentences[index:index + self.max_sentences_per_chunk]))
        return chunks


class RecursiveChunker:
    """
    Recursively split text using separators in priority order.

    Default separator priority:
        ["\n\n", "\n", ". ", " ", ""]
    """

    DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

    def __init__(self, separators: list[str] | None = None, chunk_size: int = 500) -> None:
        self.separators = self.DEFAULT_SEPARATORS if separators is None else list(separators)
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        # TODO: implement recursive splitting strategy
        if not text or not text.strip():
            return []
        return self._split(text, self.separators)


    def _split(self, current_text: str, remaining_separators: list[str]) -> list[str]:
        # TODO: recursive helper used by RecursiveChunker.chunk
        stripped = current_text.strip()

        if not stripped:
            return []
        if len(stripped) <= self.chunk_size:
            return [stripped]

        if not remaining_separators or remaining_separators == [""]:
            return [stripped[i:i + self.chunk_size] for i in range(0, len(stripped), self.chunk_size)]

        separator, rest = remaining_separators[0], remaining_separators[1:]

        parts = stripped.split(separator)

        if len(parts) == 1:
            return self._split(stripped, rest)

        pieces = [part + separator for part in parts[:-1]] + [parts[-1]]

        chunks: list[str] = []

        buffer = ""

        def flush():
            nonlocal buffer
            if buffer:
                chunks.append(buffer.strip())
                buffer = ""
        for piece in pieces:

            if len(piece.strip()) > self.chunk_size:
                flush()
                chunks.extend(self._split(piece, rest))
                continue

            candidate = buffer + piece

            if len(candidate.strip()) <= self.chunk_size:
                buffer = candidate
            else:
                flush()
                buffer = piece

        flush()
        return chunks
        
    def _hard_split(self, text: str) -> list[str]:
        slices = (
            text[i : i + self.chunk_size].strip()
            for i in range(0, len(text), self.chunk_size)
        )
        return [s for s in slices if s]


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def compute_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    cosine_similarity = dot(a, b) / (||a|| * ||b||)

    Returns 0.0 if either vector has zero magnitude.
    """
    magnitude_a = math.sqrt(_dot(vec_a, vec_a))
    magnitude_b = math.sqrt(_dot(vec_b, vec_b))

    if magnitude_a == 0.0 or magnitude_b == 0.0:
        return 0.0

    return _dot(vec_a, vec_b) / (magnitude_a * magnitude_b)


class ChunkingStrategyComparator:
    """Run all built-in chunking strategies and compare their results."""

    def compare(self, text: str, chunk_size: int = 200) -> dict:
        strategies = {
            "fixed_size": FixedSizeChunker(chunk_size=chunk_size).chunk(text),
            "by_sentences": SentenceChunker().chunk(text),
            "recursive": RecursiveChunker(chunk_size=chunk_size).chunk(text),
        }

        comparison = {}
        for name, chunks in strategies.items():
            comparison[name] = {
                "count": len(chunks),
                "avg_length": (
                    sum(len(chunk) for chunk in chunks) / len(chunks)
                    if chunks
                    else 0.0
                ),
                "chunks": chunks,
            }

        return comparison
