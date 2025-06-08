from pydantic import BaseModel, Field, model_validator

from app.schemas.pyobjectid import PyObjectId
from app.schemas.component_schema import Cpu, Gpu, Motherboard, PowerSupply, Ram
from app.rules_engine import rule_registrar


class Build(BaseModel):
    cpu: Cpu | None = None
    ram: Ram | None = None
    motherboard: Motherboard | None = None
    gpu: Gpu | None = None
    psu: PowerSupply | None = None

    model_config = {
        "validate_assignment": True,  # валідуємо й при зміні атрибутів
    }

    @model_validator(mode="after")
    def _validate_build(cls, build):
        # Запускаємо rules engine
        rule_registrar.run(build)
        return build


class Chat(BaseModel):
    # id: PyObjectId = Field(alias="_id")

    user_id: PyObjectId
    build: Build = Field(default_factory=Build)
    chat: list[dict | None] = Field(default_factory=list)

    @property
    def _id(self):
        return PyObjectId(self.id)
