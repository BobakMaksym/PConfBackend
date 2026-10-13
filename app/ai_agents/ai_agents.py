from agents import (
    Agent,
    handoff,
    ModelSettings,
    FunctionTool,
)
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

from app.services.ai_tools import (
    add_component,
    find_cpu,
    find_gpu,
    find_ram,
    find_motherboard,
    find_psu,
    find_ssd,
    get_configuration,
)
from app.schemas.pc_config_schema import PcConfigContext
from app.prompt.configurator import CONFIGURATOR_PROMPT
from app.prompt.question import QUESTION_PROMPT
from app.prompt.answering_question import ANSWERING_QUESTIONS_PROMPT
from app.prompt.router import ROUTER_PROMPT
from app.ai_agents.guardrails import input_guardrail_agent
from app.ai_agents.handoff import on_handoff_configurator, on_handoff_questioner


tools_4_find_components: list[FunctionTool] = [
    find_cpu,
    find_gpu,
    find_ram,
    find_motherboard,
    find_psu,
    find_ssd,
]


configurator_agent = Agent[PcConfigContext](
    model="gpt-4.1-mini",
    name="configurator",
    instructions=CONFIGURATOR_PROMPT,
    handoff_description="Picks out components based on user requirements",
    #
    # reset_tool_choice=False,
    # tool_use_behavior=StopAtTools(stop_at_tool_names=["add_component"]),
    reset_tool_choice=True,
    tool_use_behavior="run_llm_again",
    #
    tools=[
        add_component,
        get_configuration,
        *tools_4_find_components,
    ],
    input_guardrails=[input_guardrail_agent],
    model_settings=ModelSettings(
        temperature=0.5,
        top_p=0.4,
        tool_choice="required",
    ),
)


answering_questions_agent = Agent[PcConfigContext](
    model="gpt-4.1-mini",
    name="answering_questions",
    instructions=ANSWERING_QUESTIONS_PROMPT,
    tools=tools_4_find_components,
    model_settings=ModelSettings(
        temperature=0.5,
        top_p=0.4,
        tool_choice="auto",
    ),
)


questions_agent = Agent[PcConfigContext](
    model="gpt-4.1-mini",
    name="questioner",
    instructions=QUESTION_PROMPT,
    model_settings=ModelSettings(temperature=0.6, top_p=0.4),
)


# router_agent = configurator_agent

router_agent = Agent[PcConfigContext](
    name="Router",
    model="gpt-4.1-nano",
    instructions=prompt_with_handoff_instructions(ROUTER_PROMPT),
    input_guardrails=[input_guardrail_agent],
    handoffs=[
        handoff(
            agent=configurator_agent,
            tool_name_override="configurator_agent",
            tool_description_override="assembles the PC according to the user's requirements",
            on_handoff=on_handoff_configurator,
        ),
        handoff(
            questions_agent,
            tool_name_override="questions_agent",
            tool_description_override="asks questions to better understand the user's PC requirements",
            on_handoff=on_handoff_questioner,
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
