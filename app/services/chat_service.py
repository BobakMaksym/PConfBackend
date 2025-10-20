from agents import Runner, TResponseInputItem, function_tool, trace
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.ai_agents.ai_agents import router_agent
from app.core.config import settings
from app.prompt.messages import START_MESSAGE
from app.schemas.pc_config_schema import PcConfigContext
from app.schemas.chat_schema import ChatSchema
from app.repos import chat_repo


COMPONENT_COUNT = 2


class ChatService:

    async def send_message(
        self, chat_id: MongoObjectId, message: str
    ) -> TResponseInputItem:
        """pass messages with history to the agent, saves responses"""

        # build_id == chat_id
        build_id = chat_id
        build = PcConfigContext(id=build_id)

        chat = chat_repo.get_chat(chat_id)
        messages = chat.messages

        with trace(settings.WORKFLOW_NAME, chat.trace_id) as trace_obj:
            messages.append({"role": "user", "content": message})

            response = await Runner.run(router_agent, messages, context=build)

            # повне перезаписування історії повідомлень
            # це потрібно буде виправити пізніше
            all_messages = response.to_input_list()
            chat_repo.col.find_one_and_update(
                {"_id": chat_id}, {"$set": {"messages": all_messages}}
            )
        return all_messages[-1]  # response (last message)
