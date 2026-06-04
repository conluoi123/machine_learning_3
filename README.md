# SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks

## Giới thiệu dự án

Đây là dự án thực hành môn **Nhập môn Học máy** (Đại học Khoa học Tự nhiên, ĐHQG-HCM).

Dự án mô phỏng và cài đặt từ đầu (built from scratch) thuật toán **SmoothLLM** nhằm bảo vệ các Mô hình Ngôn ngữ Lớn (LLMs) trước các đòn tấn công bẻ khóa (Jailbreak Attacks). Thuật toán được cài đặt dựa trên bài báo nghiên cứu:

> _Robey, A., Wong, E., Hassani, H., & Pappas, G. J. (2023). "[SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks](https://arxiv.org/abs/2310.03684)"_

**Cơ chế hoạt động chính:** Hệ thống phòng thủ hoạt động theo dạng Hộp đen (Black-box), tạo ra nhiều bản sao bị làm nhiễu (Perturbations: Insert, Swap, Patch) từ câu lệnh của người dùng, đưa qua LLM, sau đó dùng thuật toán **Bỏ phiếu đa số (Majority Vote)** và cơ chế **LLM-as-a-judge** để quyết định chặn (Block) hay cho phép (Pass) câu trả lời.

---

## 🛠 Yêu cầu hệ thống (Prerequisites)

Để chạy được dự án này, máy tính của bạn cần có:

- **Python:** Phiên bản 3.8 trở lên.
- **API Key:** Có tài khoản và API Key hợp lệ của Google Gemini (miễn phí tại Google AI Studio) hoặc cài đặt sẵn Ollama nếu muốn chạy mô hình Local.

---

## Hướng dẫn cài đặt (Installation)

**Bước 1: Clone kho lưu trữ về máy**

```bash
git clone git@github.com:conluoi123/machine_learning_3.git
cd machine_learning_3
```

**Bước 2: Tạo và kích hoạt môi trường ảo (Khuyên dùng)**

```bash
# Tạo môi trường ảo có tên là venv
python -m venv venv

# Kích hoạt trên Windows:
venv\Scripts\activate

# Kích hoạt trên macOS/Linux:
source venv/bin/activate
```

**Bước 3: Cài đặt các thư viện cần thiết**

```bash
pip install -r requirements.txt
```

---

## Cấu hình API Key (Configuration)

Để mã nguồn chạy được mà không lộ khóa bảo mật, dự án sử dụng biến môi trường.

1. Trong thư mục gốc, tạo một file mới có tên là `.env` (hoặc copy từ file `.env.example` nếu có).
2. Mở file `.env` và điền API Key của bạn vào theo định dạng sau:

```env
GEMINI_API_KEY=AIzaSyYourSecretAPIKeyHere...
```

_(**Lưu ý Bảo mật:** Tuyệt đối không commit file `.env` lên GitHub. File này đã được thêm vào `.gitignore` để đảm bảo an toàn)._

---

## Hướng dẫn chạy code (Usage)

Dự án được chia thành các script riêng biệt. Khởi chạy theo thứ tự sau để xem toàn bộ kết quả:

### 1. Chạy thực nghiệm chính (So sánh Baseline vs SmoothLLM)

Lệnh này sẽ chạy 10 câu lệnh độc hại qua LLM gốc (không phòng thủ) để tính Base ASR, sau đó chạy qua hệ thống SmoothLLM để thấy tỷ lệ bị chặn.

```bash
python main.py
```

### 2. Chạy phân tích siêu tham số (Ablation Study)

Lệnh này phân tích sự thay đổi của hiệu suất phòng thủ khi tinh chỉnh các tham số $N$ (Số lượng bản sao) và $q$ (Tỷ lệ nhiễu).

```bash
python ablation.py
```

### 3. Vẽ biểu đồ trực quan hóa

Sau khi 2 lệnh trên chạy xong và sinh ra file JSON trong thư mục `data/results/`, bạn chạy lệnh sau để xuất biểu đồ phân tích:

```bash
python visualize.py
```

---

## Kết quả kỳ vọng (Expected Results)

Sau khi chạy thành công các lệnh trên, bạn sẽ quan sát thấy:

1. **Trên Terminal:** Log hệ thống in ra từng kịch bản, thanh tiến trình `tqdm` chạy phần trăm, kèm theo thông báo `[BLOCKED]` nếu phát hiện tấn công, hoặc `[SAFE]` nếu prompt an toàn. Cuối cùng, tỷ lệ **ASR (Attack Success Rate)** của 2 kịch bản sẽ được in ra để so sánh.
2. **Thư mục `data/results/`:** Sẽ tự động xuất hiện các file `baseline_results.json`, `smoothllm_results.json` và `ablation_results.json` chứa dữ liệu thô.
3. **Biểu đồ trực quan:** Lệnh visualize sẽ tạo ra các file ảnh định dạng `.png` trong thư mục `results/`, thể hiện rõ ràng sự suy giảm của tỷ lệ ASR nhờ vào lớp phòng thủ SmoothLLM so với Baseline, rất phù hợp để dán trực tiếp vào Slide báo cáo.

---

_Dự án thực hiện bởi nhóm sinh viên ĐH KHTN (HCMUS)._
