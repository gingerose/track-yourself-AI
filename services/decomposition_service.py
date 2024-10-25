from transformers import GPT2LMHeadModel, GPT2Tokenizer
import openai

# model = GPT2LMHeadModel.from_pretrained("gpt2")
# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

openai.api_key = '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'

def Decompose_task(task_description, min_points=6, max_points=10):
    response = openai.Completion.create(
        model="o1-preview",
        prompt=f"Decompose the task '{task_description}' into {min_points} to {max_points} steps.",
        temperature=0.9,
        max_tockens=200,
        stop=["\n", " Human:", " AI:"],
    )
    return response
    # try:
    #     prompt = f"Decompose the task '{task_description}' into {min_points} to {max_points} steps."

    #     inputs = tokenizer.encode_plus(prompt, return_tensors="pt", padding=True, truncation=True)
    #
    #     outputs = model.generate(inputs['input_ids'], attention_mask=inputs['attention_mask'], max_length=150, num_return_sequences=1)
    #
    #     steps = tokenizer.decode(outputs[0], skip_special_tokens=True)
    #
    #
    #     return steps.split('\n'), None
    #
    # except Exception as e:
    #     return None, str(e)
