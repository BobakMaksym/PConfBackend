from agents import Agent, handoff, ModelSettings
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

from app.ai_tools import (
    add_component,
    find_cpu,
    find_gpu,
    find_ram,
    find_motherboard,
    find_psu,
    get_configuration,
)
from app.schemas.build import BuildContext
from app.prompt.configurator import CONFIGURATOR_PROMPT
from app.prompt.question import QUESTION_PROMPT
from app.prompt.answering_question import ANSWERING_QUESTIONS_PROMPT
from app.prompt.router import ROUTER_PROMPT


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
    tools=[
        find_cpu,
        find_gpu,
        find_ram,
        find_motherboard,
        find_psu,
    ],
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


router_agent = Agent[BuildContext](
    name="Router",
    model="gpt-4.1-nano",
    instructions=prompt_with_handoff_instructions(ROUTER_PROMPT),
    handoffs=[
        handoff(
            configurator_agent,
            tool_name_override="configurator_agent",
            tool_description_override="assembles the PC according to the user's requirements",
        ),
        handoff(
            questions_agent,
            tool_name_override="questions_agent",
            tool_description_override="asks questions to better understand the user's PC requirements",
        ),
        handoff(
            answering_questions_agent,
            tool_name_override="answering_questions_agent",
            tool_description_override="provides answers to user questions",
        ),
    ],
    model_settings=ModelSettings(
        temperature=0.2,
        top_p=0.2,
        tool_choice="required",
    ),
)
