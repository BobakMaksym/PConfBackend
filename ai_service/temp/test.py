import torch
import transformers
from transformers import AutoTokenizer

# Завантажуємо токенізатор
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")

# Додаємо системне повідомлення вручну
SYSTEM_PROMPT = """<|start_header_id|>system<|end_header_id|>

You are a helpful AI assistant. Answer concisely and informatively.

<|eot_id|>
"""

# Ініціалізуємо пайплайн
pipe = transformers.pipeline(
    "text-generation",
    model="meta-llama/Llama-3.2-1B-Instruct",
    tokenizer=tokenizer,
    model_kwargs={
        "torch_dtype": torch.float16,
        "quantization_config": {"load_in_4bit": True},
        "low_cpu_mem_usage": True,
        "max_position_embeddings": 131072
    }
)

# Стоп-токени
STOP_TOKENS = [128000, 128009]

def chat():
    conversation = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chatbot. Goodbye!")
            break

        # Формуємо історію чату
        chat_history = "\n".join(
            [f"<|start_header_id|>{msg['role']}<|end_header_id|>\n{msg['content']}<|eot_id|>" for msg in conversation]
        )
        
        # Додаємо поточний запит користувача
        prompt = f"{chat_history}\n<|start_header_id|>user<|end_header_id|>\n{user_input}<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>\n"

        # Генеруємо відповідь
        output = pipe(prompt, max_new_tokens=150, eos_token_id=STOP_TOKENS, temperature=0.7, top_p=0.9)

        # Обробка відповіді
        response = output[0]["generated_text"][len(prompt):].strip()
        print(f"Assistant: {response}")

        # Додаємо відповідь в історію діалогу
        conversation.append({"role": "user", "content": user_input})
        conversation.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    chat()
