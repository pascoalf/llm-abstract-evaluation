import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, GenerationConfig

model = None
pipe = None
tokenizer = None

def prepare_model(select_model):
    global model, pipe, tokenizer
    #
    tokenizer = AutoTokenizer.from_pretrained(select_model)

    # Load model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(
        select_model, #e.g., "microsoft/Phi-3-mini-4k-instruct",
        device_map = "auto",
        torch_dtype = "auto",
        attn_implementation="eager"
    )

    generation_config = GenerationConfig(  
        max_new_tokens=5)

    # create a pipeline
    pipe = pipeline(
        "text-generation",
        model = model,
        tokenizer=tokenizer,
        return_full_text = False,
        generation_config = generation_config
        )

if __name__ == "__main__":
    prepare_model("microsoft/Phi-3-mini-4k-instruct")
