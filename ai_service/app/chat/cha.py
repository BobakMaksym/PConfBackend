from jinja2 import Template

from prompt.system import (
    CONSULTANT_SYSTEM_PROMPT,
    EXTRACT_FILTERS_SYSTEM_PROMPT,
    SCHEMAS,
    FILTER_EXAMPLES,
)


template = Template(EXTRACT_FILTERS_SYSTEM_PROMPT)

res = template.render(
    schemas=SCHEMAS,
    examples=FILTER_EXAMPLES,
)

print(res)


# #################################################

Response(
    id="resp_681cce0e30e48191b10b36d649ff1c1c0f4d61141b470b9d",
    instructions=None,
    output=[
        ResponseOutputMessage(
            id="msg_681cce0ead9c8191b22b46cd76ed832e0f4d61141b470b9d",
            content=[
                ResponseOutputText(
                    annotations=[],
                    text="Привіт! Я технічний консультант, який допомагає обирати компоненти для кастомних ПК. Як можу допомогти?",
                    type="output_text",
                )
            ],
            role="assistant",
            status="completed",
            type="message",
        )
    ],
    tools=[
        FunctionTool(
            name="assemble_pc",
            parameters={
                "type": "object",
                "required": [],
                "properties": {},
                "additionalProperties": False,
            },
            strict=True,
            type="function",
            description="Assembles a PC according to the user's wishes",
        )
    ],
    previous_response_id=None,
    text=ResponseTextConfig(format=ResponseFormatText(type="text")),
    user=None,
)


[
    ResponseOutputMessage(
        id="msg_681d168385608191b3c609c178c0d6aa01de4604fde0e793",
        status="completed",
        type="message",
        role="assistant",
        content=[
            ResponseOutputText(
                annotations=[],
                text="Які ще компоненти ти хотів би включити? Наприклад, тип накопичувача (SSD або HDD), материнська плата, блок живлення, корпус?",
                type="output_text",
            )
        ],
    )
]


[
    ResponseFunctionToolCall(
        id="fc_681d169f34d8819193ccf6ea3907117b01de4604fde0e793",
        status="completed",
        type="function_call",
        arguments="{}",
        call_id="call_yN2BwaCer2SlABGdHl6pTrdc",
        name="assemble_pc",
    )
]
