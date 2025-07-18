from dataclasses import dataclass

from pydantic import BaseModel, Field, model_validator

from app.schemas.component_schema import Cpu, Gpu, Ram, PowerSupply, Motherboard
from app.schemas.pyobjectid import PyObjectId
from app.rules_engine.manager import rule_manager


@dataclass
class PcConfigContext:
    _id: PyObjectId


class Components(BaseModel):
    cpu: PyObjectId | None = None
    gpu: PyObjectId | None = None
    ram: PyObjectId | None = None
    psu: PyObjectId | None = None
    motherboard: PyObjectId | None = None


class PcConfig(BaseModel):
    # To update the list of errors,
    # you need to call `update_errors` or `model_dump`

    id: PyObjectId | None = Field(alias="_id", default=None)
    user_id: PyObjectId

    cpu: Cpu | None = None
    ram: Ram | None = None
    motherboard: Motherboard | None = None
    gpu: Gpu | None = None
    psu: PowerSupply | None = None

    # when adding components dynamically, errors does not change
    errors: list[str | None] = Field(
        default_factory=list,
        description="list of component compatibility errors",
    )

    def update_errors(self) -> list[str]:
        """updates the list of errors"""
        self.errors = rule_manager.check_compatibility(self)
        return self.errors

    @model_validator(mode="after")
    def build_validator(self):
        """
        errors is initialized only when creating a Config object
        and does not change when dynamically adding attributes
        """
        self.update_errors()
        return self

    # class Config:
    #     json_encoders = {
    #         PyObjectId: lambda v: str(v),
    #     }
