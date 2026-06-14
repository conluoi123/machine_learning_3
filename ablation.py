import itertools, json
import os
import pandas as pd
from tqdm import tqdm

from config import DATA_PATH, RESULT_DIRS
from main import call_api, build_attack_prompt
from smooth_llm import smoothllm_defend
from judge import is_jailbroken

df = pd.read_csv(DATA_PATH)

ABLATION_PROMPTS = [
    build_attack_prompt(row["goal"], row["target"])
    for _, row in df.head(10).iterrows()
]

ABLATION_PROMPTS = ABLATION_PROMPTS[:5]

N_VALUES = [1, 3, 5]
Q_VALUES = [10]
METHODS = ["insert", "swap"]

def main():
    os.makedirs(RESULT_DIRS, exist_ok=True)
    ablation_data = []

    for n, q, method in tqdm(
        list(itertools.product(N_VALUES, Q_VALUES, METHODS)),
        desc="Ablation Study"
    ):
        jailbroken_count = 0
        jailbreak_rates = []

        for prompt in ABLATION_PROMPTS:
            result = smoothllm_defend(
                prompt=prompt,
                call_api_fn=call_api,
                n=n,
                q=q,
                method=method,
            )
            jailbreak_rates.append(result["jailbreak_rate"])

            if is_jailbroken(result["response"]):
                jailbroken_count += 1

        asr = jailbroken_count / len(ABLATION_PROMPTS)
        avg_jailbreak_rate = sum(jailbreak_rates) / len(jailbreak_rates)

        ablation_data.append({
            "N": n,
            "q": q,
            "method": method,
            "asr": asr,
            "avg_jailbreak_rate": avg_jailbreak_rate,
        })

        with open(f"{RESULT_DIRS}/ablation_results.json", "w", encoding="utf-8") as f:
            json.dump(ablation_data, f, ensure_ascii=False, indent=2)

        print(
            f"N={n}, q={q}%, method={method} "
            f"-> ASR={asr:.1%}, avg jailbreak rate={avg_jailbreak_rate:.1%}"
        )

    with open(f"{RESULT_DIRS}/ablation_results.json", "w", encoding="utf-8") as f:
        json.dump(ablation_data, f, ensure_ascii=False, indent=2)

    print(f"Saved ablation results to {RESULT_DIRS}/ablation_results.json")

if __name__ == "__main__":
    main()
