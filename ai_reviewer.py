import requests
import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "tiiuae/falcon-7b-instruct" 

def ask_codellama(prompt):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto"  # automatically assigns model to CPU/GPU
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=True,
        temperature=0.7,
        top_p=0.95
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# Example usage
if __name__ == "__main__":
    user_code = """
def divide(a, b):
    return a / b
    """

    prompt = f"Review the following Python function for bugs or improvements:\n```python\n{user_code}\n```"
    result = ask_codellama(prompt)
    print("CodeLlama Response:\n", result)
