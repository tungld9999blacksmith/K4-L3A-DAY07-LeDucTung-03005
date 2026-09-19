# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Lê Đức Tùng | 03005
**Nhóm:** G13
**Ngày:** 19/06/2026

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Similarity cao nghĩa là hai vector biểu diễn hai câu có nội dung/ngữ nghĩa gần nhau.

**Ví dụ có độ tương tự CAO:**
- Câu A: “Sinh viên phải đóng học phí trước ngày 30/9.”
- Câu B: “Hạn cuối để người học hoàn tất thanh toán là 30/9.”
- Tại sao tương đồng:Hai câu đều nói đến cùng nội dung hạn cuối sinh viên / người học hoàn tất thanh toán

**Ví dụ có độ tương tự THẤP:**
- Câu A:“Sinh viên đăng ký học phần trực tuyến.”
- Câu B:“Thư viện mở cửa đến 22 giờ.”
- Tại sao khác: 2 câu nói đến nôi dung khác nhau, câu 1 nói về sinh viên đăng ký học phần, câu 2 noi đến thời gian đóng cửa của thư viện

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Cosine phù hợp với text embedding vì nó đo góc giữa hai vector, tập trung vào hướng/ngữ nghĩa thay vì độ dài vector như Euclid.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:* 
> *Đáp án:* `ceil((độ_dài - overlap) / (chunk_size - overlap))`

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> độ dài = 10000 ,
> chunk_size = 500 ,
> overlap = 50

> ceil((10000 - 50) / (500 - 50))
>= ceil(9950 / 450)
>= ceil(22.11)
>= 23 chunk

> Nếu tăng `ovelap` lên 100:

>ceil((10000 - 100) / (500 - 100))
>= ceil(9900 / 400)
>= ceil(24.75)
>= 25 chunk

Overlap lớn hơn giúp giữ lại nhiều ngữ cảnh giữa hai chunk, tránh cắt mất ý ở ranh giới. Đổi lại, dữ liệu bị lặp nhiều hơn và số chunk tăng.

Nên kiểm tra lại bằng FixedSizeChunker, không chỉ tin công thức.
---


## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Hàm trước hết xử lý trường hợp chuỗi rỗng bằng cách trả về danh sách rỗng, sau đó loại khoảng trắng ở đầu/cuối và tách văn bản tại các dấu `.`, `!`, `?` khi sau dấu là khoảng trắng hoặc kết thúc chuỗi; dấu chấm trong số thập phân không bị tách nhờ điều kiện `(?<!\d)`. Các câu rỗng được bỏ qua, những câu còn lại được gom tuần tự thành từng nhóm tối đa `max_sentences_per_chunk` câu và nối bằng một khoảng trắng để tạo ra các chunk.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> `chunk` loại bỏ đầu vào rỗng hoặc chỉ gồm khoảng trắng rồi gọi `_split` với danh sách separator theo thứ tự ưu tiên: `\n\n`, `\n`, `. `, ` ` và cuối cùng là chuỗi rỗng. `_split` trả về ngay khi phần văn bản đã ngắn hơn hoặc bằng `chunk_size`; nếu không còn separator thì chia cứng theo `chunk_size`, còn nếu vẫn còn separator thì tách theo separator hiện tại, giữ separator ở cuối mỗi phần, rồi tham lam gom các phần vào buffer mà không vượt quá kích thước chunk. Phần nào vẫn quá dài sẽ được đệ quy xử lý bằng các separator có độ ưu tiên thấp hơn.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> *Viết 2-3 câu: lưu trữ thế nào? Tính độ tương tự ra sao?*

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> *Viết 2-3 câu: lọc (filter) trước hay sau? Xóa bằng cách nào?*

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> *Viết 2-3 câu: cấu trúc prompt? Cách đưa ngữ cảnh (inject context) vào thế nào?*

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
# Dán kết quả (output) của: pytest tests/ -v
```

**Số lượng bài test vượt qua (pass):** __ / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | | | cao / thấp | | |
| 2 | | | cao / thấp | | |
| 3 | | | cao / thấp | | |
| 4 | | | cao / thấp | | |
| 5 | | | cao / thấp | | |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> *Viết 2-3 câu:*

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** __ / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> *Viết 2-3 câu:*

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | / 5 |
| Hướng tiếp cận của tôi (My Approach) | / 10 |
| Hoàn thiện code (Core Implementation — tests) | / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | / 5 |
| Kết quả truy xuất của tôi (Competition Results) | / 10 |
| **Tổng phần cá nhân** | **/ 60** |
