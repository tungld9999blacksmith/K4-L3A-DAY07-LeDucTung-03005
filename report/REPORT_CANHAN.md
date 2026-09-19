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
tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED                                                                                                             [  2%]
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED                                                                                                                      [  4%]
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED                                                                                                               [  7%]
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED                                                                                                                [  9%]
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED                                                                                                                     [ 11%]
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED                                                                                                     [ 14%]
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED                                                                                                           [ 16%]
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED                                                                                                            [ 19%]
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED                                                                                                          [ 21%]
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED                                                                                                                            [ 23%]
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED                                                                                                            [ 26%]
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED                                                                                                                       [ 28%]
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED                                                                                                                   [ 30%]
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED                                                                                                                             [ 33%]
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED                                                                                                    [ 35%]
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED                                                                                                        [ 38%]
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED                                                                                                  [ 40%]
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED                                                                                                        [ 42%]
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED                                                                                                                            [ 45%]
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED                                                                                                              [ 47%]
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED                                                                                                                [ 50%]
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED                                                                                                                      [ 52%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED                                                                                                           [ 54%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED                                                                                                             [ 57%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED                                                                                                 [ 59%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED                                                                                                              [ 61%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED                                                                                                                       [ 64%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED                                                                                                                      [ 66%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED                                                                                                                 [ 69%]
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED                                                                                                             [ 71%]
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED                                                                                                        [ 73%]
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED                                                                                                            [ 76%]
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED                                                                                                                  [ 78%]
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED                                                                                                            [ 80%]
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED                                                                                         [ 83%]
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED                                                                                                       [ 85%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED                                                                                                      [ 88%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED                                                                                          [ 90%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED                                                                                                     [ 92%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED                                                                                              [ 95%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED                                                                                    [ 97%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED

========================================================================================== 42 passed in 0.49s==========================================================================================
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | "Sinh viên phải nộp học phí trước hạn chót." | "Hạn cuối thanh toán học phí là mốc bắt buộc mà người học cần tuân thủ." | cao | cao | ✓ |
| 2 | "Thư viện mở cửa đến 21:00 mỗi ngày." | "Sinh viên đăng ký học phần trên cổng học vụ." | thấp | thấp | ✓ |
| 3 | "Một học phần có thể yêu cầu môn tiên quyết." | "Đăng ký học phần bắt buộc phải thỏa điều kiện tiên quyết." | cao | cao | ✓ |
| 4 | "Kỳ thi cuối kỳ bắt đầu vào tháng 12." | "Sinh viên cần lập kế hoạch mua giáo trình trước ngày 10/9." | thấp | thấp | ✓ |
| 5 | "Hệ thống hỗ trợ cần phản hồi trong 48 giờ." | "Yêu cầu hỗ trợ của người học được xử lý trong vòng hai ngày làm việc." | cao | cao | ✓ |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Cặp 1 và cặp 3 là những trường hợp đáng ngạc nhiên vì chúng không dùng cùng một từ khóa nhưng vẫn mang cùng ý nghĩa. Điều này cho thấy embedding không chỉ so khớp từ vựng đơn thuần, mà cố gắng biểu diễn khái niệm và mối quan hệ ngữ nghĩa. Kết quả cũng cho thấy các câu có chủ đề khác nhau dù có vài từ chung vẫn có thể đi thấp, do điểm mạnh của cosine phụ thuộc vào hướng vector chứ không phải thứ tự chữ cái hay từ khóa.
---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Sinh viên đăng ký học phần cần kiểm tra điều kiện gì trước khi xác nhận? | Chương trình học phần có môn tiên quyết và hướng dẫn điều chỉnh lịch học. | 2 | Có | Agent trả lời đúng: cần kiểm tra môn tiên quyết và lịch trùng, sau đó xác nhận đăng ký theo lịch. |
| 2 | Người dùng cần mang gì khi đến mượn sách ở thư viện? | Thẻ định danh hợp lệ và thủ tục mượn tài liệu của thư viện. | 2 | Có | Agent trả lời đúng: cần mang thẻ định danh hợp lệ, tuân thủ quy định mượn và thời hạn trả sách. |
| 3 | Khi phát sinh lỗi trùng lịch, sinh viên nên làm gì? | Hướng dẫn điều chỉnh lớp học phần trước thời hạn công bố. | 2 | Có | Agent giải thích đúng: điều chỉnh lớp học phần trước mốc thời hạn, và mọi yêu cầu ngoại lệ gửi qua kênh hỗ trợ chính thức. |
| 4 | Các quy định thư viện có nói gì về thời hạn trả sách? | Các thông tin về thời hạn mượn, gia hạn và xử lý quá hạn. | 1 | Có | Agent nêu được khái niệm thời hạn, nhưng chưa nêu rõ chi tiết mức phạt/vi phạm. |
| 5 | Câu hỏi cần lọc metadata để tránh nhầm lẫn giữa nội dung dành cho sinh viên và giảng viên. | Chỉ trả về nội dung phù hợp với đối tượng được lọc. | 2 | Có | Agent trả lời đúng theo hướng đối tượng mục tiêu, không bị lẫn với document của nhóm khác. |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** __ / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> Qua demo, tôi nhận ra rằng chunking strategy quyết định rất lớn đến độ “liên quan” của kết quả truy xuất. Một số câu hỏi dễ trả lời đúng hơn khi dùng chunk theo câu hoặc theo đoạn văn có cấu trúc, còn một số câu hỏi khác cần metadata lọc để tránh lấy tài liệu sai đối tượng. Bài học lớn nhất là: không chỉ chọn embedding tốt, mà còn phải chọn cách tách chunk và lọc metadata đúng với loại câu hỏi.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 9 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 8 / 10 |
| **Tổng phần cá nhân** | **57 / 60** |
