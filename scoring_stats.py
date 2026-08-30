import matplotlib.pyplot as plt
import pandas as pd

# read data
results = pd.read_csv("results/scores.csv")

# Plot clarity scores
plt.plot(results["clarity"], marker = "o")
plt.ylim(0, 5)
plt.xlabel("Abstract")
plt.ylabel("Clarity score")
plt.title("LLM clarity scores")
plt.legend("Figure 1")
plt.show()

# Bar plot option
plt.bar(results.index, results["clarity"])
plt.ylim(0, 5)
plt.xlabel("Abstract")
plt.ylabel("Clarity score")
plt.title("LLM clarity scores")
plt.legend("Figure 2")
plt.show()

#
plt.hist(results["clarity"], bins=6)
plt.xlabel("Clarity score")
plt.ylabel("Frequency")
plt.title("Distribution of clarity scores")
plt.legend("Figure 3")
plt.show()

#
ranked_clarity = results.sort_values("clarity")

plt.figure(figsize = (10, 8))
plt.barh(ranked_clarity["title"], ranked_clarity["clarity"])
plt.xlim(0, 5)
plt.xlabel("Clarity scoore")
plt.title("LLM clarity score")
plt.tight_layout()
plt.legend("Figure 4")
plt.show()