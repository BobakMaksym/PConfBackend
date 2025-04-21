import os
import json
from openai import OpenAI

from prompts import PROMPT


class Model:
    llama = "llama"
    deepseek = "deepseek"
    gpt = "gpt"


LLM_CONFIG = {
    Model.llama: {
        "model": "llama3.2:1b",
        "API_KEY": "ollama",
        "API_BASE": "http://localhost:11434/v1",
    },
    Model.deepseek: {
        "model": "deepseek-r1:1.5b",
        "API_KEY": "deepseek",
        "API_BASE": "http://localhost:11434/v1",
    },
    Model.gpt: {
        "model": "gpt-4o-mini",
        "API_KEY": "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",
    },
}

MODEL = Model.gpt

LLM = LLM_CONFIG[MODEL]

client = OpenAI(
    api_key=LLM.get("API_KEY"),
)

# Налаштування доступу до локального сервера Ollama або OpenAI-сумісного API
if LLM.get("API_BASE"):
    client.base_url = LLM.get("API_BASE")


def get_filters_from_prompt(user_input):
    system_message = PROMPT
    # """
    #     You are an assistant that extracts the characteristics for building a PC from a user request
    #     and returns them in JSON format. Possible keys: "cpu", 'pc_type', 'ssd',
    #     'case_color', 'price', 'ram', etc. If a field is not mentioned, do not add it.

    #     Example:
    #     User: "build an Intel gaming PC with 500 GB SSD in a white case for up to 25,000"
    #     Your answer:
    #     {"cpu":"intel","pc_type":"en-US","ssd":"500GB","case_color":"white","price":25000}

    #     Return ONLY the JSON object, no additional text.
    #     """

    try:
        response = client.chat.completions.create(
            model=LLM.get("model"),  # Використовуй актуальну назву моделі
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
            max_tokens=1000,
            # temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    while True:
        user_input = input(
            "\nВведіть вимоги до конфігурації ПК (або 'exit' для виходу): "
        )
        if user_input.lower() == "exit":
            break

        config_json_str = get_filters_from_prompt(user_input)

        # print("\nОтримана JSON конфігурація:")
        print(f"filters: {config_json_str}")

        # try:

        #     config_dict = json.loads(config_json_str)
        #     print("\nРозібрані фільтри:", config_dict)
        # except json.JSONDecodeError:
        #     print("Не вдалося розпізнати JSON. Сировий вивід:", config_json_str)


if __name__ == "__main__":
    main()
