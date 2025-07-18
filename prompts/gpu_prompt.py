SCHEMA = """
gpu collection schema:
  _id: ObjectID
  manufacturer: str. it's a vendor, exmpl:Asus,INNO3D
  "GPU manufacturer" str. exmpl: Intel,AMD,NVIDIA
  "GPU model": str. exmpl:"NVIDIA GeForce RTX 4070 Ti SUPER","Intel Arc B580"
  "product name": str. exmpl:"INNO3D GeForce RTX 4070 Ti SUPER TWIN X2 OC"
  "Memory size": int
  Fans: int
  Lighting: bool
  HDMI: int
  DisplayPort: int
  "Monitors connection": int
"""
# "Memory type": str. exmpl:GDDR7,GDDR6X
# "Max. resolution": str. exmpl:3840x2160,7680x4320


EXAMPLE = """
User: "Looking for an NVIDIA gpu with at least 12 GB of memory and three fans."
Response:
```json
{"GPU model":{"$regex":"nvidia","$options":"i"},"Memory size":{"$gte":12},"Fans":3}
```
User: "Give me a top-tier nvidia msi card with 16GB of memory or more for gaming and 4K resolution."
Response: 
```json
{"manufacturer": {"$regex": "msi", "$options": "i" }, "GPU manufacturer": {"$regex": "nvidia", "$options": "i" }, "Memory size": {"$gte": 16}}
```
User: "i'm building a pc with two monitors and want a rtx 3060 gpu"
Response:
```json
{"GPU model": {"$regex": "rtx 3060", "$options": "i"}, "Monitors connection": {"$gte": 2}}
```"""


USER_REQUEST = (
    "Give me a GPU that supports 8K output and has both HDMI and DisplayPort."
)


SYSTEM_PROMPT_TEMPLATE = f"""
You are a technical consultant at a computer component store, who helps customers choose a GPU for a custom PC.
Your task is to understand the customer's wishes, create a query to mongodb for the data schema below to get the right GPU.
{SCHEMA}
Examples of user request and consultant response:
{EXAMPLE}
User: {USER_REQUEST}
Response:"""


print(SYSTEM_PROMPT_TEMPLATE)
