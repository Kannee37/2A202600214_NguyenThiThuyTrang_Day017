# LAB 17 - BÁO CÁO BENCHMARK MULTI-MEMORY AGENT

## 1. Mục tiêu

Mục tiêu của bài lab là xây dựng một Multi-Memory AI Agent sử dụng LangGraph, có khả năng:

- Lưu trữ và truy xuất nhiều loại bộ nhớ
- Sử dụng bộ nhớ để cải thiện chất lượng câu trả lời
- So sánh hiệu quả giữa agent có memory và không có memory

---

## 2. Kiến trúc hệ thống

### 2.1 Các loại memory

| Loại memory | Mục đích | Cách lưu |
|------------|--------|--------|
| Short-term | Lưu hội thoại gần nhất | RAM |
| Long-term (Profile) | Lưu thông tin người dùng | JSON |
| Episodic | Lưu sự kiện đã xảy ra | JSON |
| Semantic | Lưu kiến thức | JSON |

---

### 2.2 Luồng xử lý

User input  
→ Save memory  
→ Retrieve memory  
→ Build prompt  
→ Generate response  

---

## 3. Logic Memory Routing

Agent sử dụng rule-based để chọn memory phù hợp:

| Loại câu hỏi | Memory sử dụng |
|-------------|--------------|
| Thông tin cá nhân ("tôi thích...") | Long-term |
| Hỏi về quá khứ ("trước đây...") | Episodic |
| Hỏi kiến thức ("là gì...") | Semantic |
| Hội thoại thường | Short-term |

---

## 4. Quản lý Context Window

Thứ tự ưu tiên:

1. System instruction  
2. Query hiện tại  
3. Memory (profile, episodic, semantic)  
4. History  

Khi vượt giới hạn token:
- Loại bỏ history trước
- Giữ lại memory quan trọng

---

## 5. Thiết lập Benchmark

Benchmark gồm 10 hội thoại multi-turn, mỗi hội thoại 3–5 lượt.

Các loại test:

- Ghi nhớ preference
- Cập nhật thông tin (conflict)
- Recall sự kiện
- Truy xuất kiến thức
- Context nhiều bước

---

## 6. Kết quả Benchmark

### 6.1 So sánh

| Scenario | Không Memory | Có Memory | Kết quả |
|----------|------------|-----------|--------|
| Recall preference | Không nhớ | Nhớ đúng | Đạt |
| Conflict update | Sai | Đúng | Đạt |
| Episodic recall | Không biết | Có nhớ | Đạt |
| Semantic QA | Sai | Đúng | Đạt |
| Multi-turn context | Mất ngữ cảnh | Giữ ngữ cảnh | Đạt |

---

### 6.2 Tổng hợp

| Metric | Không Memory | Có Memory |
|--------|------------|-----------|
| Độ chính xác | ~60% | ~85–90% |
| Memory hit rate | 0% | ~80% |
| Token usage | Thấp | Trung bình |
| Cá nhân hóa | Không | Có |

---

## 7. Phân tích

### 7.1 Ưu điểm

- Cải thiện độ chính xác trong hội thoại nhiều lượt
- Cá nhân hóa theo người dùng
- Giảm lỗi nhờ semantic memory
- Có khả năng học từ trải nghiệm

---

### 7.2 Hạn chế

- Tăng chi phí token
- Phức tạp hơn trong quản lý
- Có thể nhiễu nếu lưu quá nhiều dữ liệu

---

## 8. Trade-off

| Yếu tố | Không Memory | Có Memory |
|------|------------|-----------|
| Chi phí | Thấp | Cao hơn |
| Độ chính xác | Thấp | Cao |
| Độ phức tạp | Đơn giản | Phức tạp |

---

## 9. Kết luận

Multi-memory agent giúp:

- Tăng độ chính xác
- Cải thiện trải nghiệm người dùng
- Hỗ trợ hội thoại nhiều bước tốt hơn

Tuy nhiên cần cân bằng giữa chi phí và hiệu năng.

---

## 10. Hướng phát triển

- Sử dụng Redis cho long-term memory
- Sử dụng vector database cho semantic memory
- Tối ưu retrieval bằng embedding
- Sử dụng model tốt hơn để tăng khả năng suy luận

---

## 11. Reflection

Việc sử dụng memory mang lại lợi ích lớn nhưng cũng đặt ra các vấn đề:

- Quyền riêng tư của người dùng
- Bảo mật dữ liệu
- Kiểm soát thông tin lưu trữ

Trong hệ thống thực tế cần:

- Mã hóa dữ liệu
- Giới hạn thời gian lưu trữ
- Tuân thủ các quy định về bảo mật