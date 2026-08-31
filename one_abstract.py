import create_pipeline as cp
from datasets import load_dataset

cp.prepare_model("microsoft/Phi-3-mini-4k-instruct")

abstracts = load_dataset(
    "slinusc/PubMedAbstractsSubset",
    split="train",
    streaming=True
)

some_abstracts = list(abstracts.take(20))

# first example
abstract = some_abstracts[1]["abstract"]

# simple prompt
eval_abstract1 = [
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
                    {abstract}
                """
    }
]

query1 = cp.pipe(eval_abstract1, 
                 do_sample=True, 
                 top_p=0.5, 
                 temperature = 0.1, 
                 clean_up_tokenization_spaces=False)

#
print("""Response to prompt below:
|
|
|
""")
print(query1[0]["generated_text"])
