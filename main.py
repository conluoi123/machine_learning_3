import pandas as pd 
import json, os, time 
from tqdm import tqdm 
import google.generativeai as genai 
from config import * 
from smooth_llm import smoothllm_defend, perturb
from judge import is_jailbroken 
import requests
from google.api_core.exceptions import ResourceExhausted

# setup api
genai.configure(api_key = GEMINI_API_KEY)
model = genai.GenerativeModel(LLM_MODEL) 

## gemini -> bị rate limit 
def call_api(prompt: str, system: str = None) -> str:  
    for attempt in range(10): 
        try: 
            full_prompt = f"{system}\n\n{prompt}" if system else prompt 
            response = model.generate_content(full_prompt)
            time.sleep(4) 
            return response.text 
            
        except ResourceExhausted:
            print(f"  [Rate Limit] Bị chặn. Đang ngủ 60 giây để hồi API... (Lần {attempt+1})")
            time.sleep(60)
        except Exception as e: 
            print(f"  [Lỗi khác] {e}")
            time.sleep(5)
            
    return "[API ERROR] Failed to get response"

# sd local ollama 
def call_ollama(prompt: str, system: str=None) -> str: 
    '''
        Gọi Local LLM thông qua Ollama 
    '''
    url = "http://localhost:11434/api/generate"
    OLLAMA_MODEL = "qwen2.5-coder:1.5b-base"
    payload = {
        "model": OLLAMA_MODEL, 
        "prompt": f"{system}\n\n{prompt}" if system else prompt, 
        "stream": False
    }

    try: 
        response = requests.post(url, json=payload)
        response.raise_for_status() 
        return response.json()["response"]
    except requests.exceptions.ConnectionError: 
        return "[ERROR] Không thể kết nối tới Ollama. Hãy bật Ollama lên."
    except Exception as e: 
        print(f" [Ollama Error]: {e}")
        return "[API ERROR] Failed to get response from Ollama"



df = pd.read_csv(DATA_PATH)
prompts = df["goal"].tolist()[:10]

os.makedirs(RESULT_DIRS, exist_ok=True)

# Baseline - không có phòng thủ 
print("\n" + "="*60)
print("[BASELINE] — LLM không có phòng thủ")
print("="*60)
baseline_results = []
for prompt in tqdm(prompts, desc="Baseline"):
    response  = call_api(prompt)
    # response = call_ollama(prompt)
    jailbroken = is_jailbroken(response) 
    baseline_results.append({
        "prompt":    prompt[:80] + "...",
        "response":  response[:200],
        "jailbroken": jailbroken,
    })
# ASR
baseline_asr = sum(r["jailbroken"] for r in baseline_results) / len(baseline_results)
print(f"\nBaseline ASR: {baseline_asr:.1%}  ({sum(r['jailbroken'] for r in baseline_results)}/{len(baseline_results)} jailbroken)")
with open(f"{RESULT_DIRS}/baseline_results.json", "w", encoding="utf-8") as f:
    json.dump({"asr": baseline_asr, "results": baseline_results}, f, ensure_ascii=False, indent=2)


# SmoothLLM defense
print("\n" + "="*60)
print(f"[SMOOTHLLM] — N={N_COPIES}, q={Q_PERCENT}%, method=swap")
print("="*60)
smoothllm_results = []
for prompt in tqdm(prompts, desc="SmoothLLM"):
    result = smoothllm_defend(
        prompt      = prompt,
        call_api_fn = call_api,
        # call_api_fn=call_ollama,
        n           = N_COPIES,
        q           = Q_PERCENT,
        method      = "swap",
        gamma       = GAMMA,
    )
    
    smoothllm_results.append({
        "prompt":        prompt[:80] + "...",
        "blocked":       result["blocked"],
        "jailbreak_rate": result["jailbreak_rate"],
        "verdict":       result["verdict"],
    })

smoothllm_asr = sum(not r["blocked"] and r["jailbreak_rate"] > 0 
                    for r in smoothllm_results) / len(smoothllm_results)
print(f"\n SmoothLLM ASR: {smoothllm_asr:.1%}  (đã block {sum(r['blocked'] for r in smoothllm_results)}/{len(smoothllm_results)} tấn công)")
with open(f"{RESULT_DIRS}/smoothllm_results.json", "w", encoding="utf-8") as f:
    json.dump({"asr": smoothllm_asr, "results": smoothllm_results}, f, ensure_ascii=False, indent=2)
print(f"\n Hoàn thành! Xem kết quả tại thư mục {RESULT_DIRS}")