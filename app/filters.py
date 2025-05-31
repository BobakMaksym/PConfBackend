from typing import TypeAlias

from pydantic import BaseModel, Field, model_validator


def field(desc: str = None, ex: list[str] = None, *args, **kwargs) -> Field:
    """returns `pydantic.Field(default=None, *args, **kwargs)`"""

    if desc:
        kwargs["description"] = desc
    if ex:
        kwargs["examples"] = ex

    return Field(default=None, *args, **kwargs)


Int: TypeAlias = int | None
Bool: TypeAlias = bool | None
Str: TypeAlias = str | None


class IntRange(BaseModel):
    gte: Int = field(alias="$gte", desc="greater than or equal")
    lte: Int = field(alias="$lte", desc="less than or equal")


class In(BaseModel):
    in_: list[str] = field(
        alias="$in",
        desc="value of a field equals any value in the specified array",
    )


StrOrIn: TypeAlias = str | In | None
IntOrIn: TypeAlias = int | IntRange | None


class CpuFilters(BaseModel):
    manufacturer: StrOrIn = None
    socket: Str = field(ex=["amd am4", "intel lga 1700"])
    ram_types: Str = field(ex=["ddr5"])

    cores: IntOrIn = field(ex=[8, {"$gte": 6, "$lte": 12}])
    threads: IntOrIn = field(ex=[16, {"$gte": 8, "$lte": 32}])

    model: Str = field(ex=["amd ryzen 7 9800x"])
    igp: Bool = None


class GpuFilters(BaseModel):
    manufacturer: StrOrIn = None
    model: Str = field(ex=["gigabyte radeon rx 7700 xt gaming oc"])
    fans: IntOrIn = field(ex=[1, 2, 3, {"$gte": 1, "$lte": 2}])
    memory_size: IntOrIn = field(ex=[12, {"$gte": 16, "$lte": 24}])

    model_gpu: Str = None
    lighting: Bool = None


class RamFilters(BaseModel):
    manufacturer: StrOrIn = None
    # model: Str = field(ex=["g.skill aegis ddr4 2x16gb f4-2400c15d-32gis"])

    type: Str = field(ex=["ddr4", "ddr5"])
    modules: Int = field(ex=[1, 2, 4], desc="quantity of modules")
    capacity: Int = field(ex=[8, 16, 32], desc="memory capacity (GB)")
    speed: IntRange = field(
        ex=[{"$gte": 3600, "$lte": 6000}], desc="memory speed (MHz)"
    )

    lighting: Bool = None
    # cooling: Bool = None
    # colour: Str = None


class MotherboardFilters(BaseModel):
    manufacturer: StrOrIn = None
    # model: Str = field(ex=["asus tuf gaming b550m-plus (90mb14a0-m0eay0)"])

    socket: Str = field(ex=["amd am4", "intel lga 1700"])
    form_factor: Str = field(ex=["micro-atx", "atx", "e-atx", "mini-itx"])
    ram_type: Str = field(ex=["ddr4", "ddr5"])
    ram_slots: Int = field(ex=[2, 4], desc="number of slots for RAM")
    m2_count: Int = field(ex=[1, 2], desc="number of slots for M2 SSDs")

    chipset: Str = field(ex=["intel h410", "amd b840"])

    # lighting: Bool = None
    # vrm_heatsink: Bool = None
    # wifi: Bool = None


class PsuFilters(BaseModel):

    manufacturer: StrOrIn = None
    # model: Str = field(ex=["be quiet! pure power 12 m bn341"])
    form_factor: Str = field(ex=["atx", "sfx"])
    power: IntOrIn = field(ex=[600, {"$gte": 800, "$lte": 1100}])

    efficiency: IntOrIn = field(ex=[85, {"$gte": 88, "$lte": 90}])
    certification: Str = field(ex=["80+ gold", "80+ silver", "80+"])

    # mb_and_cpu_powersupply: Str = None
    # plus_12v: Int = field(ex=[600, {"$gte": 800, "$lte": 1100}])
    # pci_e_8pin_6_2: Int = None
    # pci_e_16pin: Int = None
    # pci_e_6pin: Int = None
    # pci_e_8pin: Int = None

    # декор
    # cable_system: Str = None
    # cooling_system: Str = None
    # fan_bearing: Str = None

    # інфа
    # manufacturers_warranty: Int = None
    # dimensions: Str = None


if __name__ == "__main__":

    filters = CpuFilters(
        cores={"$gte": 6, "$lte": 12},
        manufacturer={"$in": ["intel", "amd"]},
    ).model_dump(exclude_none=True, by_alias=True)
    print(filters)

    filters = CpuFilters(
        cores=10,
        manufacturer="intel",
    ).model_dump(exclude_none=True, by_alias=True)
    print(filters)
