CPU_SCHEMA = """CPU schema:
  _id: ObjectID
  manufacturer: enum. exmpl: Intel | AMD
  fuzzy model: str. exmpl: Intel Core i3 Raptor Lake Refresh 14100F
  Series: str. exmpl: Ryzen 7, Xeon, Core Ultra 5
  Cores: int
  Threads: int
  IGP: bool
  Socket: str. exmpl: AMD AM5, Intel LGA 1200"""


GPU_SCHEMA = """GPU schema:
  _id: ObjectID
  manufacturer: str. exmpl: Asus, INNO3D
  fuzzy model: str. exmpl: "INNO3D GeForce RTX 4070 Ti SUPER TWIN X2 OC"
  GPU manufacturer: enum. exmpl: Intel | AMD | NVIDIA
  Memory size: int
  Fans: int
  Lighting: bool
  Monitors connection: int"""


SCHEMAS = [
    CPU_SCHEMA,
    GPU_SCHEMA,
]
