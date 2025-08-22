from pydantic import BaseModel, Field, model_validator
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.schemas.component_schema import Cpu, Gpu, Ram, PowerSupply, Motherboard
from app.rules_engine.manager import rule_manager
from app.schemas.base import BaseDbModel


class PcConfigId(BaseDbModel):
    pass


class PcConfigContext(BaseDbModel):
    """PC config context"""


class Components(BaseModel):
    cpu: MongoObjectId | None = None
    gpu: MongoObjectId | None = None
    ram: MongoObjectId | None = None
    psu: MongoObjectId | None = None
    motherboard: MongoObjectId | None = None


class PcConfig(BaseDbModel):
    # To update the list of errors,
    # you need to call `update_errors` or `model_dump`

    user_id: MongoObjectId

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
