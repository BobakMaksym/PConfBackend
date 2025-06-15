import json
from agents import Runner, TResponseInputItem, function_tool, trace

from app.ai_agents import router_agent
from app.core.config import settings
from app.db import db
from app.helpers import COLLECTIONS
from app.prompt.messages import START_MESSAGE
from app.schemas.build import BuildContext
from app.schemas.chat_schema import ChatSchema
from app.schemas.pyobjectid import PyObjectId
from app.repo import BuildRepo, ChatRepo


COMPONENT_COUNT = 2


build_repo = BuildRepo(db)
chat_repo = ChatRepo(db)


async def send_message_to_chat(chat_id: PyObjectId, message: str) -> TResponseInputItem:
    """pass messages with history to the agent, saves responses"""

    # build_id == chat_id
    build_id = chat_id
    build = BuildContext(_id=build_id)

    chat_doc = chat_repo.get_chat(chat_id)
    chat = ChatSchema(**chat_doc)
    messages = chat.messages

    with trace(settings.WORKFLOW_NAME, chat.trace_id) as trace_obj:
        messages.append({"role": "user", "content": message})

        response = await Runner.run(router_agent, messages, context=build)

        # повне перезаписування історії повідомлень
        # це потрібно буде виправити пізніше
        chat_repo.col.find_one_and_update(
            {"_id": chat_id}, {"$set": {"messages": response.to_input_list()}}
        )
    return response.final_output
