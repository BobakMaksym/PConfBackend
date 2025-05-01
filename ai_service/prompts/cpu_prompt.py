# CPU_SCHEMA = """
# collection: cpu_converted
#   + columns
#     _id: ObjectId
#     manufacturer: str # example: intel, amd
#     cores: int # example: 4, 6
#     threads: int # example: 8, 14
#     igp: str # True or False
#     socket: str # example: "Intel LGA 1700", "AMD AM5"
#     ram types: list[str] # supported memory types, example: [DDR3], [DDR4, DDR5]
#     product title: str # full name of the cpu, contains manufacturer, model, package, part number. example: "AMD Ryzen 7 Phoenix 8700G BOX (100-100001236BOX)", "Intel Core Ultra 5 Arrow Lake 245KF OEM (AT8076806414)"
#     purpose_category: list[str] # example: [office, gaming, general, workstation, server]
#     performance_level: str # example: low, mid, high
# """


# CPU_SCHEMA = """
# cpu collection schema:
#   _id: ObjectID
#   manufacturer: str: intel
#   "product title": str: Intel Core i3 Raptor Lake Refresh 14100F OEM (CM8071505092207)
#   Series: str: Ryzen 7, Xeon, Core Ultra 5
#   Cores: int
#   Threads: int
#   IGP: bool
#   Socket: str: AMD AM5
#   ram_types: list[str]: [DDR4,DDR5]
#   performance_level: enum: mid|low|high
#   purpose_category: list[str]: [gaming,office,general,workstation,server]
# """


CPU_SCHEMA = """
cpu collection schema:
  _id: ObjectID
  manufacturer: str. exmpl: intel, amd
  product title: str. exmpl: Intel Core i3 Raptor Lake Refresh 14100F OEM
  Series: str. exmpl: Ryzen 7, Xeon, Core Ultra 5
  Cores: int
  Threads: int
  IGP: bool
  Socket: str. exmpl: AMD AM5, Intel LGA 1200
  RAM types: list[str]. exmpl: [DDR4,DDR5], [DDR5]
"""
# performance_level: enum. exmpl: mid|low|high
# Purpose category: list[str]. exmpl: [gaming,office,general,workstation,server]


EXAMPLE = """
User: "I want a very powerful cpu for gaming and video editing, with at least 8 cores and integrated graphics, the processor should be amd"
Response:
```json
{"manufacturer": {"$regex": "amd", "$options": "i"}, "Cores": {"$gte": 8}, "IGP": true}
```
User: "I need a simple processor for office tasks with lga 1200 socket"
Response: 
```json
{"Socket": {"$regex": "lga 1200", "$options": "i"}}
```"""


USER_REQUEST = "want an average processor to work with 3d and video editing, and sometimes I will play minecraft"


SYSTEM_PROMPT_TEMPLATE = f"""
You are a technical consultant at a computer component store, who helps customers choose a processor for a custom PC.
Your task is to understand the customer's wishes, create a query to mongodb for the data schema below to get the right processors.
{CPU_SCHEMA}
Examples of user request and consultant response:
{EXAMPLE}
User: {USER_REQUEST}
Response:"""


print(SYSTEM_PROMPT_TEMPLATE)
