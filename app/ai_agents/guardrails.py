import logging
from datetime import datetime

from agents import (
    Agent,
    GuardrailFunctionOutput,
    # InputGuardrailTripwireTriggered,
    ModelSettings,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)
from pydantic import BaseModel, Field

from app.schemas.pc_config_schema import PcConfigContext


logger = logging.getLogger("app")


class ValidQuery(BaseModel):
    is_pc_question: bool
    conclusion: str = Field(
        description="whether the question about a PC",
        examples=["questions about processors", "questions about history"],
    )


guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you about PC",
    output_type=ValidQuery,
    model="gpt-4.1-nano",
    model_settings=ModelSettings(
        temperature=0.5,
        top_p=0.4,
    ),
)


@input_guardrail
async def input_guardrail_agent(
    ctx: RunContextWrapper[PcConfigContext],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    logger.debug("спрацював")

    result = await Runner.run(starting_agent=guardrail_agent, input=input, context=ctx)

    start = datetime.now()

    logger.debug(
        "time: %s; питання про ПК: %s; output: %s",
        datetime.now() - start,
        result.final_output.is_pc_question,
        result.final_output.conclusion,
    )
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_pc_question,
    )
