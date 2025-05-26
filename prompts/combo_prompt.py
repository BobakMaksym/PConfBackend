from jinja2 import Template


CPU_SCHEMA = """CPU collection schema:
  _id: ObjectID
  manufacturer: enum. exmpl: Intel | AMD
  fuzzy model: str. exmpl: Intel Core i3 Raptor Lake Refresh 14100F
  Series: str. exmpl: Ryzen 7, Xeon, Core Ultra 5
  Cores: int
  Threads: int
  IGP: bool
  Socket: str. exmpl: AMD AM5, Intel LGA 1200
"""
# product title: str. exmpl: Intel Core i3 Raptor Lake Refresh 14100F OEM
# RAM types: list[str]. exmpl: [DDR4,DDR5], [DDR5]

GPU_SCHEMA = """GPU collection schema:
  _id: ObjectID
  manufacturer: str. it's a vendor, exmpl: Asus, INNO3D
  fuzzy model: str. exmpl: "INNO3D GeForce RTX 4070 Ti SUPER TWIN X2 OC"
  GPU manufacturer: enum. exmpl: Intel | AMD | NVIDIA
  Memory size: int
  Fans: int
  Lighting: bool
  Monitors connection: int
"""
# product name: str. exmpl:"INNO3D GeForce RTX 4070 Ti SUPER TWIN X2 OC"
# GPU model: str. exmpl:"NVIDIA GeForce RTX 4070 Ti SUPER","Intel Arc B580"
# HDMI: int
# DisplayPort: int


ex = [
    {
        "User": "I want a quiet and productive computer to work with video and photos. Preferably an Intel core i5 13th generation processor with iGPU, at least 12 threads. The video card should be NVIDIA from MSI or Asus with support for 2 monitors and 8 GB of memory.",
        "Response": {
            "cpu": {
                "manufacturer": "Intel",
                "fuzzy model": "Intel core i5 13th",
                "Threads": {"$gte": 12},
                "IGP": True,
            },
            "gpu": {
                "GPU manufacturer": "NVIDIA",
                "fuzzy model": "NVIDIA MSI|NVIDIA Asus",
                "Monitors connection": {"$gte": 2},
                "Memory size": 8,
            },
        },
    },
    {
        "User": "I need an inexpensive PC for gaming and studying. Processor preferably AMD ryzen 5 3600 with 6 cores. Video card such as RTX 3050 or 3060, without backlight and a maximum of 2 fans",
        "Response": {
            "cpu": {
                "manufacturer": "AMD",
                "fuzzy model": "AMD ryzen 5 3600",
                "Cores": 6,
            },
            "gpu": {
                "fuzzy model": "rtx 3050|rtx 3060",
                "Lighting": {"$ne": True},
                "Fans": {"$lte": 2},
            },
        },
    },
    {
        "User": "I want a stylish and powerful computer for streaming and video editing. Intel Core i7 or something from the new Ultra, preferably with LGA1700 socket. Video card - NVIDIA 40 series with 12+ GB, support for 4 HDMI and without a noisy cooler.",
        "Response": {
            "cpu": {
                "manufacturer": "Intel",
                "fuzzy model": "Intel core i7 ultra",
                "Series": {"$regex": "core i7|ultra 7", "$options": "i"},
                "Socket": "LGA 1700",
            },
            "gpu": {
                "GPU manufacturer": "NVIDIA",
                "fuzzy model": "NVIDIA 40",
                "Memory size": {"$gte": 12},
            },
        },
    },
    {
        "User": "I need a work computer for CAD and 3D graphics. I want an AMD Ryzen 7 with 8 cores and integrated graphics. Video card - without backlight, support for 3 monitors, preferably AMD or Intel, but not NVIDIA.",
        "Response": {
            "cpu": {
                "manufacturer": "AMD",
                "fuzzy model": "AMD Ryzen 7",
                "Series": {"$regex": "ryzen", "$options": "i"},
                "Cores": 8,
                "IGP": True,
            },
            "gpu": {
                "fuzzy model": "AMD|Intel",
                "Lighting": {"$ne": True},
                "Monitors connection": {"$gte": 3},
                "GPU manufacturer": {"$in": ["AMD", "Intel"]},
            },
        },
    },
    {
        "User": "compact but good computer for general use and movies",
        "Response": {
            "general_requirements": "compact, beautiful PC for general use and movies",
        },
    },
]


USER_DATA = {
    "general_requirements": "workstation for CAD and 3D; CPU: AMD Ryzen, 8 cores with IGP; GPU: AMD or NVIDIA, not Intel, without backlight, support for 3 monitors",
    "cpu": {
        "manufacturer": {"$regex": "amd", "$options": "i"},
        "Series": {"$regex": "ryzen", "$options": "i"},
        "cores": 8,
        "IGP": True,
    },
    "gpu": {
        "Lighting": False,
        "Monitors connection": {"$gte": 3},
        "GPU manufacturer": {"$in": ["AMD", "NVIDIA"], "$nin": ["Intel"]},
    },
}

# USER_DATA = {
#     "general_requirements": "workstation for CAD and 3D; CPU: AMD Ryzen, 8 cores with IGP; GPU: AMD or NVIDIA, not Intel, without backlight, support for 3 monitors, with more than 8 GB of video memory",
#     "cpu": {
#         "manufacturer": "AMD",
#         "Series": {"$regex": "ryzen", "$options": "i"},
#         "Cores": 8,
#         "IGP": True,
#     },
#     "gpu": {
#         "Lighting": False,
#         "Monitors connection": {"$gte": 3},
#         "GPU manufacturer": {"$in": ["AMD", "NVIDIA"], "$nin": ["Intel"]},
#         "Memory size": {"$gt": 8},
#     },
# }


USER_REQUEST = "I want more than 8 gb of video memory"
# USER_REQUEST = "I have a budget of $3k, and I like the atx case"


# Your task is to understand the customer's wishes, create a query to mongodb for the data schemas below to get the right components.

SYSTEM_PROMPT_TEMPLATE = """
You are a technical consultant at a PC component store, who helps customers choose components for a custom PC.
Your task is to find out from the user his wishes regarding the PC and its components and to extract filters from his answers according to the data schemes:

{{ cpu_schema }}
{{ gpu_schema }}
If the user has provided little information, you will have to find out on your own in 2-3 separate questions.
The minimum information that the user should provide before you start selecting components is
- total budget
- what tasks the PC is for
- a few important characteristics, such as the number of CPU cores, RAM, video memory, SSD memory, and case format
If the user does not know what to answer the question or says that it does not matter, then this is equal to "not specified"

Here is the data that the user has already provided:
```json
{{ user_data }}
```
You should expand or modify this data as needed based on the user's replica, and you MUST return the data in JSON format in this response.

Examples of user request and consultant response:

{% for example in examples -%}
User: {{ example.User[:140] }}...
Response:
```json
{{ example.Response }}
```
{% endfor -%}
User: {{ user_request }}
Response:"""


template = Template(SYSTEM_PROMPT_TEMPLATE)
text = template.render(
    cpu_schema=CPU_SCHEMA,
    gpu_schema=GPU_SCHEMA,
    user_data=USER_DATA,
    examples=ex,
    user_request=USER_REQUEST,
)
print(text)
