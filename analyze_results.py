import pandas as pd

all_results = pd.read_csv("results/all_models_15seed_20abstracts_3prompts.csv")

# Group by model and title

# Final score stats -- overall
all_results.groupby(["model"])["final_score"].mean()
all_results.groupby(["model"])["final_score"].std()