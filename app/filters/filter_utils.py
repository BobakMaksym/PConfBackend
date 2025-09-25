from enum import StrEnum
from types import new_class
from typing import ClassVar, Literal, Optional, Type, Iterable

from fastapi_filter.contrib.mongoengine import Filter
from mongoengine import Document
from pydantic import ConfigDict
from pydantic_extra_types.mongo_object_id import MongoObjectId


class FilterLookup(StrEnum):
    EXACT = "exact"
    CONTAINS = "contains"
    IN = "in"
    GTE = "gte"
    LTE = "lte"


FieldSuffix = Literal["exact", "contains", "in", "gte", "lte"]


def get_annotations_from_model(model: Type[Document]):
    annotations = model.__annotations__
    annotations["id"] = MongoObjectId
    for cls in model.__mro__:
        if cls is Document:
            break
        annotations.update(cls.__annotations__)
    return annotations


def create_filter_class(
    model: Type[Document],
    fields: dict[str, Iterable[FieldSuffix]],
) -> Type[Filter]:

    model_fields = get_annotations_from_model(model)

    annotations = {}
    default_values = {}

    for f_name, f_values in fields.items():
        for f_value in f_values:

            f_name_full = f_name

            if f_value != "exact":
                f_name_full = f"{f_name}__{f_value}"

            if f_value == "in":
                annotations[f_name_full] = Optional[list[model_fields[f_name]]]
                default_values[f_name_full] = None
                continue

            annotations[f_name_full] = Optional[model_fields[f_name]]
            default_values[f_name_full] = None

    def init_class_namespace(ns: dict):
        """Function for initializing the class namespace"""

        ns["__module__"] = __name__

        class Constants(Filter.Constants): ...

        Constants.model = model

        ns["__annotations__"] = annotations
        ns["__annotations__"]["Constants"] = ClassVar[type]
        ns["__annotations__"]["model_config"] = ClassVar[type]

        ns.update(default_values)
        ns["Constants"] = Constants
        ns["model_config"] = ConfigDict(str_to_lower=True)

    new_filter_class = new_class(
        name=f"{model.__class__.__name__}Filters",
        bases=(Filter,),
        kwds={},
        exec_body=init_class_namespace,
    )

    return new_filter_class
