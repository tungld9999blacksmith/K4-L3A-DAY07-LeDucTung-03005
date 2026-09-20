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
| 1 | Học phí năm học 2026 của sinh viên đại học là bao nhiêu? | Mức tiền học của sinh viên khóa mới năm 2026 là bao nhiêu? | cao | 0.9136 | Đúng |
| 2 | Thời hạn nộp tiền học kỳ mùa thu kết thúc vào ngày 15 tháng 10. | Hạn chót đóng học phí kỳ 1 là ngày 15/10/2024. | cao | 0.8833 | Đúng |
| 3 | Trường hợp sinh viên rút học phần sẽ được hoàn trả 80% học phí. | Chính sách hoàn tiền khi sinh viên hủy đăng ký môn học trong tuần đầu. | cao | 0.8148 | Đúng |
| 4 | Quy định biểu phí đào tạo và phương thức chuyển khoản ngân hàng. | Thực đơn món ăn trưa tại căng tin ký túc xá hôm nay. | thấp | 0.5897 | Đúng |
| 5 | Điều kiện duy trì học bổng toàn phần yêu cầu điểm GPA tối thiểu 3.2. | Nhiệt độ ngoài trời tại Hà Nội hôm nay là 28 độ C. | thấp | 0.5192 | Đúng |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Điểm số ở cặp 4 và 5 tuy "thấp" tương đối nhưng vẫn đạt ngưỡng ~0.52 - 0.58 chứ không về 0. Điều này cho thấy các mô hình Dense Embedding hiện đại ánh xạ văn bản vào một không gian phân bố dày đặc, nơi các câu đều chia sẻ những thành phần ngữ pháp chung của ngôn ngữ tự nhiên. Tuy nhiên, khoảng cách phân tách giữa cặp tương đồng (0.81 - 0.91) và cặp dị biệt (0.51 - 0.58) đủ lớn để thuật toán cosine ranking phân loại chính xác.
---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---:|---|---|---:|---|---|
| 1 | Trong năm học 2026–2027, học phí niêm yết mỗi tín chỉ của chương trình Cử nhân Điều dưỡng, Bác sĩ Y khoa và các ngành cử nhân khác lần lượt là bao nhiêu? | Bảng học phí cử nhân năm học 2026–2027, nêu học phí theo tín chỉ của Điều dưỡng, Bác sĩ Y khoa và các ngành cử nhân khác. | 2 | Có | Agent trả lời đúng: Điều dưỡng là **9.780.000 VNĐ/tín chỉ**; Bác sĩ Y khoa và các ngành cử nhân khác là **27.195.000 VNĐ/tín chỉ**. |
| 2 | Sinh viên VinUni được hưởng khoản hỗ trợ 35% học phí từ Tập đoàn Vingroup trong thời gian bao lâu và khoản hỗ trợ này bao gồm những đối tượng nào? | Chính sách hỗ trợ 35% học phí của Nhà sáng lập, áp dụng cho sinh viên trúng tuyển nhập học trong toàn bộ thời gian học chính khóa. | 2 | Có | Agent trả lời đúng: Khoản hỗ trợ được duy trì **cố định và liên tục trong toàn bộ thời gian học chính khóa**, áp dụng cho cả sinh viên Việt Nam và sinh viên quốc tế. |
| 3 | Nghiên cứu sinh Tiến sĩ Khoa học Máy tính tại VinUni phải trả tổng học phí bao nhiêu cho toàn khóa 4 năm và có thể nhận được những quyền lợi học bổng nào? | Tài liệu học phí sau đại học, nêu tổng học phí chương trình PhD Khoa học Máy tính và chính sách học bổng nghiên cứu sinh. | 2 | Có | Agent trả lời đúng: Tổng học phí là **3.729.600.000 VNĐ/4 năm**. Nghiên cứu sinh đạt chuẩn có thể nhận **học bổng 100% học phí**, sinh hoạt phí nghiên cứu hàng tháng và bảo hiểm y tế khi tham gia TA hoặc RA. |
| 4 | Nếu sinh viên VinUni nộp đơn xin thôi học trong tuần thứ 3 của học kỳ hoặc sau tuần thứ 4, sinh viên được hoàn trả bao nhiêu phần trăm học phí thực đóng? | Chính sách hoàn phí theo thời điểm rút hồ sơ: 50% trước hoặc trong tuần thứ 4 và 0% sau tuần thứ 4. | 2 | Có | Agent trả lời đúng: Nộp đơn trong **tuần thứ 3** được hoàn **50% học phí thực đóng**; nộp sau tuần thứ 4 thì **không được hoàn trả**, tương đương 0%. |
| 5 | Khi chuyển khoản học phí bằng Việt Nam Đồng, sinh viên cần chuyển tiền đến tài khoản nào và phải ghi những thông tin gì trong nội dung chuyển khoản? | Quy định chuyển khoản VND, nêu tên đơn vị thụ hưởng, số tài khoản, ngân hàng và nội dung chuyển khoản bắt buộc. | 2 | Có | Agent trả lời đúng: Chuyển vào tài khoản **19034362262995** của **Công ty TNHH Giáo dục và Đào tạo VinAcademy** tại **Techcombank – Hội sở chính**; nội dung phải gồm **Mã số sinh viên, Họ tên sinh viên và mô tả khoản nộp**. |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 5 / 5 (100%)

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
