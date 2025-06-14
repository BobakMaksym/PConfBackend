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

from app.ai_agents import router_agent
from app.schemas.pyobjectid import PyObjectId
from app.schemas.build import BuildContext


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
    asyncio.run(main)
