from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from src.chunking import RecursiveChunker
from src.models import Document
from src.store import EmbeddingStore
from src.embeddings import _mock_embed

DATA_DIR = Path(__file__).resolve().parent / "data" / "university"
QUERIES: list[dict[str, Any]] = [
    {
        "question": "Sinh viên đóng học phí theo căn cứ nào?",
        "filter": {"audience": "student"},
        "gold": "Mỗi học kỳ, sinh viên đóng học phí theo số tín chỉ đăng ký và mức học phí theo khóa học, chương trình đào tạo.",
    },
    {
        "question": "Thời hạn thanh toán học phí của sinh viên là khi nào?",
        "filter": {"audience": "student"},
        "gold": "Sinh viên phải nộp học phí theo lịch do phòng tài chính thông báo; nếu chưa hoàn tất trước khi nhập học sẽ bị khóa quyền đăng ký mới.",
    },
    {
        "question": "Nếu sinh viên không nộp học phí thì sẽ bị xử lý thế nào?",
        "filter": {"audience": "student"},
        "gold": "Sinh viên bị khóa quyền đăng ký học phần mới và không được nhận kết quả học tập.",
    },
    {
        "question": "Những trường hợp nào được miễn hoặc giảm học phí?",
        "filter": {"audience": "student"},
        "gold": "Sinh viên thuộc diện chính sách xã hội, đạt thành tích xuất sắc hoặc được cấp học bổng theo quy định.",
    },
    {
        "question": "Học phí của cán bộ nhân viên được tính theo tiêu chí nào?",
        "filter": {"audience": "staff"},
        "gold": "Đối với nhân sự, học phí được tính theo từng khóa học và mức hỗ trợ theo quy định nội bộ, không áp dụng bảng học phí của sinh viên chính quy.",
    },
]


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return YAML-like frontmatter and the markdown body.

    The lab metadata is a flat ``key: value`` block, so a full YAML
    dependency is unnecessary here.
    """
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return {}, text

    lines = normalized.splitlines()
    if len(lines) < 3:
        return {}, text

    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break

    if end_index is None:
        raise ValueError("Frontmatter starts with '---' but has no closing '---'")

    metadata: dict[str, str] = {}
    for line in lines[1:end_index]:
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")

    body = "\n".join(lines[end_index + 1 :]).strip()
    return metadata, body


def chunk_body(body: str, chunk_size: int = 450) -> list[str]:
    # Change only this line when comparing another chunking strategy.
    chunker = RecursiveChunker(chunk_size=chunk_size)
    chunks = chunker.chunk(body)
    return [c.strip() for c in chunks if c and c.strip()]


def load_markdown_documents(base_dir: Path) -> list[Document]:
    docs: list[Document] = []
    for markdown_file in sorted(base_dir.glob("*.md")):
        text = markdown_file.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(text)
        if not body:
            continue

        chunks = chunk_body(body)
        for index, chunk in enumerate(chunks):
            doc = Document(
                id=f"{markdown_file.stem}#{index}",
                content=chunk,
                metadata={
                    **metadata,
                    "doc_id": markdown_file.stem,
                    "source": str(markdown_file),
                    "file_name": markdown_file.name,
                },
            )
            docs.append(doc)
    return docs


def run_benchmark(data_dir: Path = DATA_DIR) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    docs = load_markdown_documents(data_dir)
    if not docs:
        raise FileNotFoundError(f"No markdown files found under: {data_dir}")

    store = EmbeddingStore(collection_name="tuition_benchmark", embedding_fn=_mock_embed)
    store.add_documents(docs)

    source_count = len({doc.metadata["doc_id"] for doc in docs})
    print(f"Loaded {len(docs)} chunks from {source_count} source files")
    print()

    for i, item in enumerate(QUERIES, start=1):
        results = store.search_with_filter(
            query=item["question"],
            top_k=3,
            metadata_filter=item["filter"],
        )
        print(f"Q{i}. {item['question']}")
        print(f"   filter={item['filter']}")
        for rank, result in enumerate(results, start=1):
            doc_id = result.get("metadata", {}).get("doc_id", "unknown")
            score = result.get("score", 0.0)
            print(f"   {rank}. score={score:.6f} doc_id={doc_id}")
            preview = result["content"][:120].replace("\n", " ")
            print(f"      {preview}...")
        print(f"   gold: {item['gold']}")
        print()


if __name__ == "__main__":
    run_benchmark()
