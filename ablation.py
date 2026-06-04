import itertools, json
from tqdm import tqdm

# Lấy hàm Gemini và data từ main.py
from main import call_api, prompts 
from smooth_llm import smoothllm_defend

# [CHẠY 10 CÂU]
ABLATION_PROMPTS = prompts[:10]

N_VALUES = [1, 3, 5]            
Q_VALUES = [5, 10, 20]          
METHODS  = ["insert", "swap"]

ablation_data = []

for n, q, method in tqdm(
    list(itertools.product(N_VALUES, Q_VALUES, METHODS)),
    desc="Ablation Study"
):
    jailbroken_count = 0
    for prompt in ABLATION_PROMPTS:
        # Gọi Gemini
        result = smoothllm_defend(prompt, call_api, n=n, q=q, method=method)
        
        if not result["blocked"]:
            jailbroken_count += 1

    asr = jailbroken_count / len(ABLATION_PROMPTS)
    ablation_data.append({"N": n, "q": q, "method": method, "asr": asr})
    print(f"  [Kết quả]: N={n}, q={q}%, method={method} -> ASR={asr:.1%}")

with open("data/results/ablation_results.json", "w", encoding="utf-8") as f:
    json.dump(ablation_data, f, indent=2)

print("\nĐã chạy xong Ablation! Xem kết quả tại: data/results/ablation_results.json")
