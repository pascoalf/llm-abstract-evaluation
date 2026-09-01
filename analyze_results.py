import pandas as pd
import matplotlib.pyplot as plt

all_results = pd.read_csv("results/all_models_15seed_20abstracts_3prompts.csv")

# Group by model and title

# Final score stats -- overall
overview = all_results.groupby(["model"])["final_score"].agg(["min", "max", "mean", "std", "median"]).reset_index()

#
plt.figure(figsize=(7, 4))
plt.errorbar(
    overview["mean"],
    overview["model"],
    xerr=overview["std"],
    fmt="o",
    capsize=3,
    linewidth = 2,
    markersize = 7
)

plt.ylabel("Final score", fontsize = 12)
plt.xticks(rotation=30, fontsize = 12)
plt.tight_layout()
#plt.savefig("results/model_scores_overall.png", dpi=300, bbox_inches="tight")
plt.show()


## by model and title
# statistics by title and model
title_stats = all_results.groupby(["model", "title"])["final_score"].agg(["min", "max", "mean", "std", "median"]).reset_index()

#
model_cols = {
    "Qwen/Qwen2.5-3B-Instruct": "blue",
    "meta-llama/Llama-3.2-3B-Instruct": "green",
    "microsoft/Phi-3-mini-4k-instruct": "orange"
}

for model in title_stats["model"].unique():
    subset = title_stats[title_stats["model"] == model]

    plt.errorbar(
        subset["title"],
        subset["mean"],
        yerr=subset["std"],
        fmt="o-",
        capsize=3,
        linewidth=2,
        markersize=7,
        color=model_cols[model],
        label=model
    )

plt.legend(fontsize = 20)
plt.xticks([])
plt.yticks(fontsize = 17)
plt.ylabel("Final score", fontsize = 17)
plt.tight_layout()
plt.show()