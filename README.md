# SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks

Đây là source code demo thực nghiệm cho Đồ án 3 môn **Nhập môn Học máy**.

Dự án cài đặt minh họa thuật toán **SmoothLLM** dựa trên bài báo:

> Robey, A., Wong, E., Hassani, H., & Pappas, G. J. (2023). *SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks*. https://arxiv.org/abs/2310.03684

Demo được thực hiện theo hướng **tự xây dựng từ đầu**: tạo prompt tấn công từ AdvBench, chạy baseline không phòng thủ, chạy SmoothLLM, tính ASR và vẽ biểu đồ kết quả.

## Thành viên nhóm

| MSSV | Họ và tên |
| --- | --- |
| 23120347 | Nguyễn Kim Quốc |
| 23120348 | Ngô Thị Thục Quyên |
| 23120390 | Cao Quốc Tuấn |
| 23120393 | Lục Hoàng Tuấn |
| 23120403 | Huỳnh Trọng Viên |

## Cấu trúc chính

```text
machine_learning_3/
|-- main.py                  # Chạy baseline và SmoothLLM
|-- smooth_llm.py            # Cài đặt perturbation và majority vote
|-- judge.py                 # Đánh giá response có bị jailbreak hay không
|-- ablation.py              # Thử nghiệm thay đổi siêu tham số
|-- visualize.py             # Vẽ biểu đồ kết quả
|-- config.py                # Cấu hình model, tham số và đường dẫn
|-- requirements.txt         # Danh sách thư viện cần cài
`-- data/
    |-- advbench_sample.csv  # Tập mẫu AdvBench
    `-- results/             # Kết quả JSON và hình biểu đồ
```

## Cài đặt

Tạo môi trường ảo, nếu cần:

```bash
python -m venv venv
```

Kích hoạt môi trường ảo trên Windows:

```bash
venv\Scripts\activate
```

Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

## Cấu hình API key

Demo chính sử dụng Gemini API. Tạo file `.env` trong thư mục chứa `main.py`:

```env
GEMINI_API_KEY=
```

Dán API key thật sau dấu `=`. Không commit file `.env` lên GitHub.

Kiểm tra API key:

```bash
python -c "from config import GEMINI_API_KEY; print(GEMINI_API_KEY is not None)"
```

Kết quả mong đợi:

```text
True
```

## Cấu hình thực nghiệm hiện tại

Các tham số chính trong `config.py`:

```python
LLM_MODEL = "gemini-3.1-flash-lite"
N_COPIES = 5
Q_PERCENT = 10
GAMMA = 0.5
SAMPLE_SIZE = 5
DEFAULT_METHOD = "swap"
PROMPT_MODE = "attack"
```

Trong đó:

- `SAMPLE_SIZE = 5`: chạy 5 mẫu AdvBench để hạn chế quota API.
- `PROMPT_MODE = "attack"`: tạo prompt tấn công thủ công từ cặp `goal-target`.
- `N_COPIES = 5`: tạo 5 bản sao perturbed cho mỗi prompt.
- `Q_PERCENT = 10`: làm nhiễu 10% ký tự.
- `DEFAULT_METHOD = "swap"`: dùng perturbation dạng thay thế ký tự trong thực nghiệm chính.

## Cách chạy

Chạy từ thư mục chứa `main.py`:

```bash
cd machine_learning_3
```

### 1. Chạy thực nghiệm chính

```bash
python main.py
```

Kết quả được lưu tại:

```text
data/results/baseline_results.json
data/results/smoothllm_results.json
```

Kết quả hiện tại:

```text
Baseline ASR:  20.0%
SmoothLLM ASR: 0.0%
```

### 2. Chạy ablation study

```bash
python ablation.py
```

Thực nghiệm hiện tại khảo sát:

```python
N_VALUES = [1, 3, 5]
Q_VALUES = [10]
METHODS = ["insert", "swap"]
```

Kết quả lưu tại:

```text
data/results/ablation_results.json
```

### 3. Vẽ biểu đồ

```bash
python visualize.py
```

Biểu đồ được lưu tại:

```text
data/results/asr_comparison.png
data/results/ablation_by_n.png
```

## Ghi chú

- Dataset sử dụng là tập mẫu **AdvBench Harmful Behaviors** trong `data/advbench_sample.csv`.
- Prompt tấn công được tạo thủ công từ `goal-target`, không phải adversarial suffix sinh bởi GCG/PAIR.
- Judge mặc định dựa trên keyword refusal để tiết kiệm API.
- Code có hàm hỗ trợ Ollama local, nhưng kết quả chính hiện tại dùng Gemini API.
- Do Gemini API có quota/rate limit, nếu bị chặn có thể giảm `SAMPLE_SIZE`, `N_COPIES` hoặc chỉ chạy lại `visualize.py`.
