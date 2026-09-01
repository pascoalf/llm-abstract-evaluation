import evaluate_model as em
from datasets import load_dataset
import time

# 
models = [
    "microsoft/Phi-3-mini-4k-instruct",
    "Qwen/Qwen2.5-3B-Instruct",
    "meta-llama/Llama-3.2-3B-Instruct"
]

abstracts = load_dataset(
            "slinusc/PubMedAbstractsSubset",
            split="train",
            streaming=True
        )

some_abstracts = list(abstracts.take(20))

    # Extract titles used
titles = [paper["title"] for paper in some_abstracts]
    # to store the results later
all_results = []

#
start = time.perf_counter()

# Run over all models, multiple seeds, all prompts
for selected_model in models:
    em.evaluate_model(select_model = selected_model, 
                      seed = 5, 
                      some_abstracts=some_abstracts,
                      titles = titles,
                      all_results = all_results,
                      file_name= "all_models_5seed_20abstracts_3prompts")

#

elapsed = time.perf_counter() - start

print(f"It took {elapsed} to run.")
