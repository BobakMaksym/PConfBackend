import os
import json
from typing import Optional, List, Dict
from datetime import datetime

from agents import Agent, Runner, function_tool
from pydantic import BaseModel, Field
from pymongo import MongoClient

from app.schemas.pyobjectid import PyObjectId


openai_api_key = os.environ.get("OPENAI_API_KEY")
mongo = MongoClient("mongodb://localhost:27017")
db = mongo["pc_parts"]


class Requirements(BaseModel):
    usage: Optional[str] = Field(None, description="gaming, design, ML …")
    budget: Optional[int] = None
    resolution: Optional[str] = None
    upgrade_plan: Optional[bool] = None


class BuildState(BaseModel):
    cpu: Optional[str] = None
    gpu: Optional[str] = None
    motherboard: Optional[str] = None
    ram: List[str] = []


class BuildService:
    def __init__(self, db):
        self.db = db

    def search_components(self, type_: str, filters: Dict, limit: int = 10):
        col = self.db[f"components.{type_}"]
        q = {"in_stock": True, **filters}
        cursor = col.find(q, {"name": 1, "price": 1}).limit(limit)
        return list(cursor)

    def get_component(self, type_: str, comp_id: str):
        col = self.db[f"components.{type_}"]
        return col.find_one({"_id": PyObjectId(comp_id)})

    def create_build(self) -> str:
        build = {"state": {}, "created_at": datetime.utcnow()}
        res = self.db["builds"].insert_one(build)
        return str(res.inserted_id)

    def load_build(self, build_id: str) -> BuildState:
        doc = self.db["builds"].find_one({"_id": PyObjectId(build_id)})
        return BuildState(**doc["state"])

    def save_build(self, build_id: str, state: BuildState):
        self.db["builds"].update_one(
            {"_id": PyObjectId(build_id)},
            {"$set": {"state": state.model_dump(), "updated_at": datetime.now()}},
        )


service = BuildService(db)


@function_tool
def search_db(component_type: str, filters: Dict) -> List[Dict]:
    """Пошук компонентів у БД за фільтрами"""
    return service.search_components(component_type, filters)


@function_tool
def add_to_build(build_id: str, component_type: str, component_id: str) -> bool:
    """Додає компонент до збірки"""
    st = service.load_build(build_id)
    setattr(st, component_type, component_id)
    service.save_build(build_id, st)
    return True


"""

You are a technical AI consultant at a PC component store, who helps customers choose components for a custom PC.
Your task is to find out in detail the client's wishes for a custom PC in 3-4 replicas and finally assemble the PC.
Avoid long answers if possible and ask only one question at a time, for example:
- What is your budget?
- What are the requirements for the PC or its characteristics?
The minimum you need to know is: price, tasks, component preferences, or
characteristics (e.g. brands, models, power, memory, color, backlight, etc.)

When you “assemble the PC”, the user may want to make changes, so you should ask if they are satisfied with everything, if so, say “Glad to help”, if not, ask a few more questions and then call the “assemble_pc” function

Answer only in Ukrainian.
"""

clarify_agent = Agent(
    name="ClarifyAgent",
    instructions=(
        "Ти — консультант, який ставить короткі уточнюючі запитання, доки не "
        "заповнить усі поля Requirements. Коли всі поля заповнено, "
        "виведи рівно один JSON із ключем requirements і нічого більше."
    ),
    model="gpt-4o",
)

build_agent = Agent(
    name="BuildAgent",
    instructions=(
        "Ти — AI-збирач ПК. Твої інструменти:\n"
        "• search_db — повертає список компонентів\n"
        "• add_to_build — додає компонент до поточної збірки\n\n"
        "Алгоритм:\n"
        "1) Для кожного типу компонента сформуй фільтри\n"
        "2) Використай search_db → обери найдешевший або найкращий\n"
        "3) add_to_build\n"
        "4) Коли збереш мінімальний сет (CPU, motherboard, GPU, RAM) — заверши відповіддю "
        "у форматі JSON з ключем build та коротким поясненням."
    ),
    model="gpt-4o",
    tools=[search_db, add_to_build],
)


def run_cli():
    print("=== PConf AI (CLI) ===\n")
    user_msg = input("Ви: ")
    while True:
        result = Runner.run_sync(clarify_agent, user_msg)
        ai_msg = result.final_output
        print(f"AI: {ai_msg}")
        try:
            data = json.loads(ai_msg)
            requirements = Requirements(**data["requirements"])
            break
        except Exception:
            user_msg = input("Ви: ")

    build_id = service.create_build()
    builder_prompt = (
        f"Ось вимоги користувача (JSON): {requirements.model_dump()}. "
        f"Поточна збірка має id '{build_id}'. Починай підбір."
    )
    result = Runner.run_sync(build_agent, builder_prompt)
    print(f"\nAI-Builder: {result.final_output}")
    print(
        "\n🎉 Готово. Щоб переглянути збережену збірку — відкрий MongoDB "
        f"колекцію 'builds' та документ {build_id}.\n"
    )


if __name__ == "__main__":
    run_cli()
