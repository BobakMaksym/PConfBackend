import asyncio
import json
import subprocess

from agents import Agent, Runner, function_tool, trace

from app.service_ai import search_components, add_component, remove_component, get_build

# CONSULTANT_SYSTEM_PROMPT = """
# Тм — консультант у магазині комплектуючих для кастомних ПК.
# Твоє завдання — визначити побажання клієнта щодо кастомного ПК у 2-3 репліках і зібрати ПК з допомогою "build_pc".
# Уникай довгих відповідей і задавай лише одне питання за раз.
# Приклади питань:
# - Який ваш бюджет?
# - Які вимоги до ПК або його характеристик?
# Мінімум, що вам потрібно знати, це: ціна, завдання, вподобання щодо компонентів або
# характеристики (наприклад, марки, моделі, потужність, пам'ять, колір, підсвічування тощо).

# Коли збереш ПК, користувач може захотіти внести зміни, тому слід запитати,
# чи все його влаштовує, якщо так, скажи "Радий був допомогти", якщо ні, то почни алгоритм спочатку.
# """
CONSULTANT_SYSTEM_PROMPT = (
    "Ти — консультант у магазині комплектуючих для кастомних ПК."
    "Твоє завдання — визначити побажання клієнта щодо кастомного ПК"
    'у 2-3 репліках і зібрати ПК з допомогою "build_pc".'
    "Уникай довгих відповідей і задавай лише одне питання за раз."
    "Приклади питань:\n"
    "- Який ваш бюджет?\n"
    "- Які вимоги до ПК або його характеристик?\n"
    "Мінімум, що вам потрібно знати, це: ціна, завдання, вподобання щодо компонентів або"
    "характеристики (наприклад, марки, моделі, потужність, пам'ять, колір, підсвічування тощо).\n"
    "Після збірки користувач може захотіти внести зміни, тому запитай,"
    'чи все його влаштовує, якщо так, скажи "Радий був допомогти",'
    'якщо ні — почни алгоритм спочатку, тобто виясни що користувач хоче змінити, після чого перезбери ПК з "build_pc".'
)


@function_tool
def build_pc():
    """збирає або перебудовує пк з урахуванням побажань користувача"""

    subprocess.run(["notify-send", '"call build_pc function"'])

    return {"cpu": "intel core i5", "gpu": "MSI RTX 3060", "ram": 16}


async def main():
    agent = Agent(
        model="gpt-4o-mini",
        name="Consultant",
        instructions=CONSULTANT_SYSTEM_PROMPT,
        tools=[search_components],  # , add_component, remove_component, get_build],
    )

    print(f"consultant: {history[0]["content"]}")

    with trace(workflow_name="Consultant") as trace_obj:
        print(trace_obj.trace_id)

        while True:

            user_input = input("you: ")
            if user_input.lower() in ("q", "quit", "exit"):

                with open("./history.json", "w+") as file:
                    json.dump(history, file, indent=2, ensure_ascii=False)

                break

            history.append({"role": "user", "content": user_input})

            result = await Runner.run(agent, history)

            print(f"consultant: {result.final_output}")

            history.append({"role": "assistant", "content": result.final_output})

    print("Buy !")


history = []
history.append(
    {
        "role": "assistant",
        "content": "Я консультант, допоможу підібрати компоненти до кастомного ПК. Які у тебе побажання?",
    }
)


if __name__ == "__main__":
    asyncio.run(main())
