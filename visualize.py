import json
import os
import pandas as pd
import matplotlib.pyplot as plt

from config import RESULT_DIRS

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def plot_asr_comparison():
    baseline = load_json(f"{RESULT_DIRS}/baseline_results.json")
    smooth = load_json(f"{RESULT_DIRS}/smoothllm_results.json")

    labels = ["Baseline", "SmoothLLM"]
    values = [baseline["asr"], smooth["asr"]]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values)
    plt.ylim(0, 1)
    plt.ylabel("Attack Success Rate")
    plt.title("Baseline vs SmoothLLM")

    for i, value in enumerate(values):
        plt.text(i, value + 0.02, f"{value:.1%}", ha="center")

    plt.tight_layout()
    plt.savefig(f"{RESULT_DIRS}/asr_comparison.png", dpi=200)
    plt.close()

def plot_ablation():
    data = load_json(f"{RESULT_DIRS}/ablation_results.json")
    df = pd.DataFrame(data)
    metric = "avg_jailbreak_rate" if "avg_jailbreak_rate" in df.columns else "asr"
    ylabel = "Average Jailbreak Rate" if metric == "avg_jailbreak_rate" else "Average ASR"

    plt.figure(figsize=(8, 5))

    for method in df["method"].unique():
        sub = df[df["method"] == method]
        grouped = sub.groupby("N")[metric].mean()
        plt.plot(grouped.index, grouped.values, marker="o", label=method)

    baseline_path = f"{RESULT_DIRS}/baseline_results.json"
    if os.path.exists(baseline_path):
        baseline = load_json(baseline_path)
        plt.axhline(
            y=baseline["asr"],
            color="red",
            linestyle="--",
            linewidth=1,
            label=f"baseline ASR ({baseline['asr']:.1%})",
        )

    plt.ylim(0, 1)
    plt.xlabel("N")
    plt.ylabel(ylabel)
    plt.title("Ablation by N and Method")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{RESULT_DIRS}/ablation_by_n.png", dpi=200)
    plt.close()

def main():
    os.makedirs(RESULT_DIRS, exist_ok=True)
    plot_asr_comparison()
    plot_ablation()
    print(f"Saved plots to {RESULT_DIRS}")

if __name__ == "__main__":
    main()
