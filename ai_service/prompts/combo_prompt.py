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
        "User": "I want a quiet and productive computer to work with video and photos. Preferably an Intel processor with iGPU, at least 12 threads. The video card should be NVIDIA with support for 2 monitors and 8 GB of memory.",
        "Response": {
            "general_requirements": "quiet and productive PC for working with video and photos",
            "cpu": {
                "manufacturer": "Intel",
                "Threads": {"$gte": 12},
                "IGP": True,
            },
            "gpu": {
                "GPU manufacturer": "NVIDIA",
                "Monitors connection": {"$gte": 2},
                "Memory size": 8,
            },
        },
    },
    {
        "User": "I need an inexpensive PC for gaming and studying. Processor preferably AMD with 6 cores. Video card such as RTX 3050 or 3060, without backlight and a maximum of 2 fans",
        "Response": {
            "general_requirements": "an inexpensive PC for gaming and studying",
            "cpu": {"manufacturer": "AMD", "Cores": 6},
            "gpu": {
                "fuzzy model": {"$regex": "rtx 3050|rtx 3060", "$options": "i"},
                "Lighting": {"$ne": True},
                "Fans": {"$lte": 2},
            },
        },
    },
    {
        "User": "I want a stylish and powerful computer for streaming and video editing. Intel Core i7 or something from the new Ultra, preferably with LGA1700 socket. Video card - NVIDIA with 12+ GB, support for 4 HDMI and without a noisy cooler.",
        "Response": {
            "general_requirements": "stylish and powerful PC for streaming and video editing, without a noisy cooler",
            "cpu": {
                "manufacturer": "Intel",
                "Series": {"$regex": "core i7|ultra", "$options": "i"},
                "Socket": "LGA 1700",
            },
            "gpu": {
                "GPU manufacturer": "NVIDIA",
                "Memory size": {"$gte": 12},
            },
        },
    },
    {
        "User": "I need a work computer for CAD and 3D graphics. I want an AMD Ryzen with 8 cores and integrated graphics. Video card - without backlight, support for 3 monitors, preferably AMD or Intel, but not NVIDIA.",
        "Response": {
            "general_requirements": "PC for CAD and 3D graphics, with AMD or Intel GPU, but not NVIDIA",
            "cpu": {
                "manufacturer": "AMD",
                "Series": {"$regex": "ryzen", "$options": "i"},
                "Cores": 8,
                "IGP": True,
            },
            "gpu": {
                "Lighting": {"$ne": True},
                "Monitors connection": {"$gte": 3},
                "GPU manufacturer": {"$in": ["AMD", "Intel"], "$nin": ["NVIDIA"]},
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


# USER_DATA = {
#     "general_requirements": "workstation for CAD and 3D; CPU: AMD Ryzen, 8 cores with IGP; GPU: AMD or NVIDIA, not Intel, without backlight, support for 3 monitors",
#     "cpu": {
#         "manufacturer": {"$regex": "amd", "$options": "i"},
#         "Series": {"$regex": "ryzen", "$options": "i"},
#         "cores": 8,
#         "IGP": True,
#     },
#     "gpu": {
#         "Lighting": False,
#         "Monitors connection": {"$gte": 3},
#         "GPU manufacturer": {"$in": ["AMD", "NVIDIA"], "$nin": ["Intel"]},
#     },
# }

USER_DATA = {
    "general_requirements": "workstation for CAD and 3D; CPU: AMD Ryzen, 8 cores with IGP; GPU: AMD or NVIDIA, not Intel, without backlight, support for 3 monitors, with more than 8 GB of video memory",
    "cpu": {
        "manufacturer": "AMD",
        "Series": {"$regex": "ryzen", "$options": "i"},
        "Cores": 8,
        "IGP": True,
    },
    "gpu": {
        "Lighting": False,
        "Monitors connection": {"$gte": 3},
        "GPU manufacturer": {"$in": ["AMD", "NVIDIA"], "$nin": ["Intel"]},
        "Memory size": {"$gt": 8},
    },
}


# USER_REQUEST = "I want more than 8 gb of video memory"
USER_REQUEST = "I have a budget of $3k, and I like the atx case"


SYSTEM_PROMPT_TEMPLATE = """
You are a technical consultant at a PC component store, who helps customers choose a CPU and GPU for a custom PC.
Your task is to understand the customer's wishes, create a query to mongodb for the data schemas below to get the right components.

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
