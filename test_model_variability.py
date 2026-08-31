import create_pipeline as cp
import re
import pandas as pd
from datasets import load_dataset
from transformers import set_seed

# run model on prompts and extract scores

# load model and prepare pipeline
cp.prepare_model("microsoft/Phi-3-mini-4k-instruct")
cp.model.generation_config.max_length = None

# load abstracts
abstracts = load_dataset(
    "slinusc/PubMedAbstractsSubset",
    split="train",
    streaming=True
)

some_abstracts = list(abstracts.take(10))

# Extract titles used
titles = [paper["title"] for paper in some_abstracts]

# to store the results later
all_results = []

for run in range(5):
    # set seed for reproducibility
    set_seed(100 + run)

    # Obtain scores
    scores_clarity = []
    scores_relevance = []
    scores_rigor = []

    for paper in some_abstracts:

        # Evaluate clarity
        eval_clarity = [
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
        # Extract clarity scoring
        scoring_clarity = cp.pipe(eval_clarity, 
                    do_sample=True, 
                    clean_up_tokenization_spaces=False)

        scores_clarity.append(scoring_clarity[0]["generated_text"])

        # Evaluate relevance
        eval_relevance = [
            {
                "role": "user",
                "content": f"""
                            Evaluate the relevance of presentation of the following scientific abstract.

                            Rate its relevance from 0 to 5, where:
                            0 = Useless
                            1 = very irrelevant
                            2 = somewhat irrelevant
                            3 = reasonably relevant
                            4 = very relevant
                            5 = exceptionally relevant

                            Return only the numerical score.

                            Abstract:
                            {paper["abstract"]}
                        """
            }
        ]
        # Extract relevance scoring
        scoring_relevance = cp.pipe(eval_relevance, 
                    do_sample=True, 
                    clean_up_tokenization_spaces=False)

        scores_relevance.append(scoring_relevance[0]["generated_text"])

        # Evaluate rigor
        eval_rigor = [
            {
                "role": "user",
                "content": f"""
                            Return only one numerical score for the apparent methodological rigor in the abstract.

                            Rate its rigor from 0 to 5, where:
                            0 = not even science
                            1 = very innacurate
                            2 = somewhat unnacurate
                            3 = reasonably rigoros
                            4 = very rigoros, minor issues only
                            5 = exceptionally rigorous

                            Abstract:
                            {paper["abstract"]}
                        """
            }
        ]
        # Extract rigor scoring
        scoring_rigor = cp.pipe(eval_rigor, 
                    do_sample=True, 
                    clean_up_tokenization_spaces=False)

        scores_rigor.append(scoring_rigor[0]["generated_text"])


    # Extract numerical score from responses
    def extract_scores(text):
        match = re.search(r"\b[0-5](?:\.5)?\b", text)
        return float(match.group()) if match else None    

    # clean the scores
    clean_scores_clarity = [extract_scores(x) for x in scores_clarity]
    clean_scores_relevance = [extract_scores(x) for x in scores_relevance]
    clean_scores_rigor = [extract_scores(x) for x in scores_rigor]

    # organize into data.frame
    results = pd.DataFrame({
        "run" : run + 1,
        "seed" : 100 + run,
        "title": titles,
        "clarity": clean_scores_clarity,
        "relevance": clean_scores_relevance,
        "rigor": clean_scores_rigor 
    })

    # Calculate final score
    results["final_score"] = results[["clarity", "relevance", "rigor"]].mean(axis = 1)

    # Join new run of results
    all_results.append(results)

    # 
    combined = pd.concat(all_results, ignore_index = True)

    #
    combined.to_csv(
        "results/repeatability.csv"
    )
