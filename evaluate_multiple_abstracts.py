import create_pipeline as cp
import re
import pandas as pd
from datasets import load_dataset

cp.main()
cp.model.generation_config.max_length = None

abstracts = load_dataset(
    "slinusc/PubMedAbstractsSubset",
    split="train",
    streaming=True
)

some_abstracts = list(abstracts.take(50))


scores = []

for paper in some_abstracts:

    # make prompt for each abstract
    eval_abstract = [
        {
            "role": "user",
            "content": f"""
                        Evaluate the clarity of presentation of the following scientific abstract.

                        Rate its clarity from 0 to 5, where:
                        0 = extremely unclear
                        1 = very unclear
                        2 = somewhat unclear
                        3 = reasonably clear
                        4 = very clear
                        5 = exceptionally clear

                        Return only the numerical score.

                        Abstract:
                        {paper["abstract"]}
                    """
        }
    ]
    # Evaluate abstract
    scoring = cp.pipe(eval_abstract, 
                 do_sample=True, 
                 clean_up_tokenization_spaces=False)

    scores.append(scoring[0]["generated_text"]) 
    #print(scoring[0]["generated_text"])

# Extract numerical score from responses
def extract_scores(text):
    match = re.search(r"\b[0-5](?:\.5)?\b", text)
    return float(match.group()) if match else None    

# clean the scores
clean_scores = [extract_scores(x) for x in scores] 

print(clean_scores)

# Extract titles used
titles = [paper["title"] for paper in some_abstracts]

# organize into data.frame
results = pd.DataFrame({
    "title": titles,
    "clarity": clean_scores 
})

print(results)
print(results["clarity"].describe())

# Store the LLM scores
results.to_csv("results/scores.csv", index = False)


raise SystemExit