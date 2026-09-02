import pandas as pd
import matplotlib.pyplot as plt

all_results = pd.read_csv("results/all_models_15seed_20abstracts_3prompts.csv")

# Group by model and title

# Final score stats -- overall
overview = all_results.groupby(["model"])["final_score"].agg(["min", "max", "mean", "std", "median"]).reset_index()

overview.to_csv("results/overview_stats.csv", index=False)

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

plt.ylabel("Final score", fontsize = 14)
plt.xticks(rotation=30, fontsize = 14)
plt.tight_layout()
plt.savefig("results/model_scores_overall.png", dpi=300, bbox_inches="tight")
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

plt.legend(fontsize = 16)
plt.xticks([])
plt.yticks(fontsize = 14)
plt.ylabel("Final score", fontsize = 14)
plt.tight_layout()
plt.savefig("results/variability_of_title_final_scores.png", dpi=300, bbox_inches="tight")
plt.show()


# Inspect divergence between models
title_stats.groupby(["title"])

models = ["Qwen/Qwen2.5-3B-Instruct", "meta-llama/Llama-3.2-3B-Instruct","microsoft/Phi-3-mini-4k-instruct"]

diverge_scores = []
#
for title in title_stats["title"].unique():
    ct = title_stats[title_stats["title"] == title]
    #
    qwen = ct[ct["model"] == models[0]]["mean"].iloc[0]
    lama = ct[ct["model"] == models[1]]["mean"].iloc[0]
    phi = ct[ct["model"] == models[2]]["mean"].iloc[0]
    #
    qwen_vs_lama = abs(qwen - lama)
    lama_vs_phi = abs(lama - phi)
    phi_vs_qwen = abs(phi - qwen)
    #
    divergence = float(max([qwen_vs_lama, lama_vs_phi, phi_vs_qwen]))
    #
    diverge_scores.append((divergence, title))
    #
    diverge_scores = sorted(diverge_scores, reverse=True)


div_scores = [x[0] for x in diverge_scores]
ranked_titles = [x[1] for x in diverge_scores]

#
plt.figure(figsize=(8, 4.5))

plt.plot(
    range(len(ranked_titles)),
    div_scores,
    marker="o",
    linewidth=2,
    markersize=5
)

plt.ylabel("Divergence score", fontsize=14)
plt.xlabel("Abstract rank", fontsize=14)

plt.xticks([])

plt.tight_layout()
plt.savefig("results/absolute_divergence_ranked.png", dpi=300, bbox_inches="tight")
plt.show()


# Analyze each score
metrics = ["clarity", "relevance", "rigor"]

fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

for ax, metric in zip(axes, metrics):

    metric_stats = (
        all_results
        .groupby(["model", "title"])[metric]
        .agg(["mean", "std"])
        .reset_index()
    )

    for model in metric_stats["model"].unique():
        subset = metric_stats[metric_stats["model"] == model]

        ax.errorbar(
            subset["title"],
            subset["mean"],
            yerr=subset["std"],
            fmt="o-",
            capsize=3,
            linewidth=2,
            markersize=5,
            color=model_cols[model],
            label=model
        )

    ax.set_title(metric.capitalize(), fontsize=16)
    ax.set_xticks([])
    ax.tick_params(axis="y", labelsize=12)

axes[0].set_ylabel("Score", fontsize=14)

axes[0].legend(fontsize=11)

plt.tight_layout()
plt.savefig(
    "results/variability_by_metric.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
