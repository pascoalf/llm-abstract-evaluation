import create_pipeline as cp

cp.prepare_model("meta-llama/Llama-3.2-3B-Instruct")

# simple prompt
test =  [{"role": "user", 
          "content": "What is your purpose?"}]

query1 = cp.pipe(test, do_sample=True, top_p=0.8, temperature = 0.1, clean_up_tokenization_spaces=False)

#
print("""Response to prompt below:
|
|
|
""")
print(query1[0]["generated_text"])
