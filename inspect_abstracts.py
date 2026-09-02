import pandas as pd
from datasets import load_dataset

abstracts = load_dataset(
            "slinusc/PubMedAbstractsSubset",
            split="train",
            streaming=True
        )

some_abstracts = list(abstracts.take(20))

some_abstracts_df = pd.DataFrame(some_abstracts)

#
print(some_abstracts_df[some_abstracts_df["title"] == "[Synthesis of N-substituted isoindolines]."]["abstract"].iloc[0])