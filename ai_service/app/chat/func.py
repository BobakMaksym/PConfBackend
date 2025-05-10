from copy import deepcopy

from openai import OpenAI

from .tool import assemble_pc


Message = dict[str]
Messages = list[Message]
Tools = list[dict[str]]


class OpenAIService:
    def __init__(
        self,
        model: str,
        system_prompt: str,
        client: OpenAI,
        tools: Tools = None,
    ):
        self.model = model
        self.system_prompt = system_prompt
        self.system_msg = {"role": "system", "content": system_prompt}
        self.tools = tools
        self.client = client

    def request(self, replica: Message, history: Messages):

        input_: Messages = deepcopy(history)
        input_.extend([self.system_msg, replica])

        response = self.client.responses.create(
            model=self.model,
            input=input_,
            text={"format": {"type": "text"}},
            reasoning={},
            tools=self.tools,
            temperature=0.4,
            max_output_tokens=2048,
            top_p=0.4,
            store=True,
        )

        return response

    @staticmethod
    def create_user_replica(text: str) -> Message:
        return {"role": "user", "content": text}


def assemble_pc_tool(service: OpenAIService, history: Messages):

    user_replica = service.create_user_replica(
        "Get absolutely all filters from previous messages."
    )
    response = service.request(user_replica, history)
