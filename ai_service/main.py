# from agents.agent import Agent
# from agents.run import Runner
# from agents.model_settings import ModelSettings

from agents import Agent, Runner, ModelSettings

from prompt.system import CONSULTANT_SYSTEM_PROMPT, EXTRACT_FILTERS_SYSTEM_PROMPT



pc_builder_agent = Agent(
    name="pc_builder_agent",
    instructions=EXTRACT_FILTERS_SYSTEM_PROMPT
)


consultant_agent = Agent(
    name="consultant_agent",
    instructions=CONSULTANT_SYSTEM_PROMPT,
    model="gpt-4o-mini",
    # tools=[],
    model_settings=ModelSettings(
        temperature=0.4,
        top_p=0.4,
        max_tokens=2048,
        tool_choice="auto",
    ),
)
