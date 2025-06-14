import asyncio
import json

from agents import (
    Agent,
    HandoffOutputItem,
    handoff,
    ItemHelpers,
    RunContextWrapper,
    MessageOutputItem,
    # RunContextWrapper,
    Runner,
    ToolCallItem,
    ToolCallOutputItem,
    TResponseInputItem,
    function_tool,
    # handoff,
    trace,
    ModelSettings,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

from app.schemas.pyobjectid import PyObjectId
from app.schemas.build import BuildContext
from app.service_ai import (
    find_cpu,
    find_gpu,
    find_ram,
    find_motherboard,
    find_psu,
    add_component,
    create_build,
    remove_component,
    get_configuration,
)
from app.prompt.configurator import CONFIGURATOR_PROMPT
from app.prompt.question import QUESTION_PROMPT
from app.prompt.answering_question import ANSWERING_QUESTIONS_PROMPT
from app.prompt.router import ROUTER_PROMPT

# CONSULTANT_SYSTEM_PROMPT = (
#     "Ти — консультант у магазині комплектуючих для кастомних ПК."
#     "Твоє завдання — визначити побажання клієнта щодо кастомного ПК"
#     'у 2-3 репліках і зібрати ПК з допомогою "build_pc".'
#     "Уникай довгих відповідей і задавай лише одне питання за раз."
#     "Приклади питань:\n"
#     "- Який ваш бюджет?\n"
#     "- Які вимоги до ПК або його характеристик?\n"
#     "Мінімум, що вам потрібно знати, це: ціна, завдання, вподобання щодо компонентів або"
#     "характеристики (наприклад, марки, моделі, потужність, пам'ять, колір, підсвічування тощо).\n"
#     "Після збірки користувач може захотіти внести зміни, тому запитай,"
#     'чи все його влаштовує, якщо так, скажи "Радий був допомогти",'
#     'якщо ні — почни алгоритм спочатку, тобто виясни що користувач хоче змінити, після чого перезбери ПК з "build_pc".'
# )

CONSULTANT_SYSTEM_PROMPT = (
    "Роби все, що каже користувач."
    'Ти не маєш права додавати пусті фільтри, як цей: `""`,'
    "чи будь-які фільтри, про які не йшла мова."
)


configurator_agent = Agent[BuildContext](
    model="gpt-4.1-mini",
    name="configurator",
    instructions=CONFIGURATOR_PROMPT,
    tools=[
        find_cpu,
        find_gpu,
        find_ram,
        find_motherboard,
        find_psu,
        add_component,
        get_configuration,
    ],
    model_settings=ModelSettings(
        temperature=0.5,
        top_p=0.4,
        tool_choice="auto",
    ),
)


answering_questions_agent = Agent[BuildContext](
    model="gpt-4.1-mini",
    name="answering_questions",
    instructions=ANSWERING_QUESTIONS_PROMPT,
    # tools=[
    #     # тут має бути інструмент для універсального пошуку компонентів по назві
    # ],
    model_settings=ModelSettings(
        temperature=0.5,
        top_p=0.4,
        tool_choice="auto",
    ),
)


questions_agent = Agent[BuildContext](
    model="gpt-4.1-mini",
    name="questioner",
    instructions=QUESTION_PROMPT,
    model_settings=ModelSettings(temperature=0.6, top_p=0.4),
)


async def main():

    build = BuildContext(_id=PyObjectId("683b7ab21fbad55848727e64"))

    history: list[TResponseInputItem] = []
    history.append(
        {
            "role": "assistant",
            "content": "Я консультант, допоможу підібрати компоненти до кастомного ПК. Які у тебе побажання?",
        }
    )

    print(f"consultant: {history[0]["content"]}")

    router_agent = Agent[BuildContext](
        name="Router",
        model="gpt-4.1-nano",
        instructions=prompt_with_handoff_instructions(ROUTER_PROMPT),
        handoffs=[
            handoff(
                configurator_agent,
                # tool_name_override="configurator_agent",
                tool_description_override="assembles the PC according to the user's requirements",
            ),
            # handoff(
            #     questions_agent,
            #     # tool_name_override="questions_agent",
            #     tool_description_override="asks questions to better understand the user's PC requirements",
            # ),
        ],
        # tools=[
        #     # configurator_agent.as_tool(
        #     #     tool_name="configurator_agent",
        #     #     tool_description="assembles the PC according to the user's requirements",
        #     # ),
        #     # questions_agent.as_tool(
        #     #     tool_name="questions_agent",
        #     #     tool_description="asks questions to better understand the user's PC requirements",
        #     # ),
        #     # answering_questions_agent.as_tool(
        #     #     tool_name="answering_questions_agent",
        #     #     tool_description="provides answers to user questions",
        #     # ),
        # ],
        model_settings=ModelSettings(
            temperature=0.2,
            top_p=0.2,
            tool_choice="required",
        ),
    )

    with trace(workflow_name="Consultant") as trace_obj:
        print(trace_obj.trace_id)

        while True:

            user_input = input("you: ")

            if user_input.lower().strip() in ("q", "quit", "exit"):
                with open("./ai_hist.json", "w+") as file:
                    json.dump(history, file, indent=2, ensure_ascii=False)
                break

            history.append({"role": "user", "content": user_input})

            """
            додав тут контекст з _id конфігурації
            """
            result = await Runner.run(router_agent, history, context=build)

            history = result.to_input_list()

            print(f"consultant: {result.final_output}")

            # кількість останніх повідомлень, що передаються як історія

            """
            якась проблема, після перевищення 40 повідомлень
            
            також тре додати до search ще інші типи компонентів
            """

            # MSG_COUNT = 10
            # history = history[-MSG_COUNT:]

            print(f"len history: {len(history)}")

    print("Buy !")


if __name__ == "__main__":
    asyncio.run(main())
