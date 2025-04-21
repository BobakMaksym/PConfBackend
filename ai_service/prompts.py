SYSTEM_PROMPT_TEMPLATE = """
Ти тех-консультант магазину комп'ютерних компонентів, який допомагає підібрати компоненти для кастомного ПК.
Твоє завдання розповісти клієнту про товари в магазині,
відповісти на його запитання, щоб у підсумку клієнт отримав список компонентів для ПК.
У діалозі з клієнтом використовуй інформацію про товари, наведену нижче.
Якщо клієнт ставить запитання, відповіді на яке немає в інформації про товари або попередніх репліках діалогу,
скажи: "У мене недостатньо інформації для відповіді на ваше запитання.".
### Уникай згадки фактів про компанію або товари, яких немає в наведеному описі.

Дотримуйся такого сценарію:
якщо не відомі призначення, задачі ПК, вподобання щодо компонентів, функціоналу, брендів, потужності,
з'ясуй їх (за кілька реплік).

Уподобання користувача: {user_info}.

Інформація про товари: {bikes_info}"
"""

# Дотримуйся такого сценарію: якщо не відомі вподобання користувача щодо типу,
# бренду та цінової категорії велосипеда, з'ясуй їх (за кілька реплік).




INSTRUCTION = """
Extract the following parameters from the customer's message:

1) Тип ПК, який потрібен користувачу. Possible purpose: gaming, office, general, workstation, server
2) Бренди компонентів (CPU, GPU, RAM).
3) Price range.
4) Power. Possible types: low, mid, high
5) Бажані моделі компонентів
6) Кольори компонентів: Possible colors: black, white, gray, red, grean, blue.
7) Кількість ядер CPU.
8) Кількість відеопам'яті у GPU.
9) Кількість RAM.
# 6) Бажані характеристики ? # НЕ ЗМОЖУ ЗРОБИТИ ДУЖЕ ДЕТАЛЬНО !

If the customer says that any of the parameters does not matter (e.g., “I don’t care”), return the value: "does not matter".

Return the result in JSON format.


Example:
User: "I need a PC to work with office programs like MS Word, and I would like an Intel processor."
Answer: {"pc type": "office", "cpu": {"manufacturer": "intel"}}


Example 1:
Customer message: “I need a mountain bike for up to 20,000 rubles, brand doesn’t matter.”
Response:
{"bike_type": "mountain", "brand": "does not matter", "price": {"<": 20000}}

Example 2:
Customer message: “I want to gift a bike to my 10-year-old son, 24 gears, wheel diameter from 22 to 24 inches.”  
Response:
{"bike_type": "kids", "num_gears": 24, "wheel_diameter": {">=": 22, "<=": 24}}

Example 3:  
Customer message: “I need a Stels bicycle for city rides, with rim brakes, from 20,000 to 25,000 rubles.”  
Response:
{"bike_type": "road", "brand": "stels", "brakes_type": "rim", "price": {">=": 20000, "<=": 25000}}
"""


############################################################################################################

PROMPT = """
You are an intelligent query parser for a PC configurator. Your task is to parse the user's text query and extract the key parameters for filtering video cards in the database.

Your actions:
Analyze the query and understand what characteristics of video cards the user is interested in.
Select the key filters and present them in JSON format.
Ignore general words such as “I need”, “I want to choose”, “advise”, “I'm looking for”.
If a parameter is not mentioned, do not include it in your response.
Don't make up values - use only what is in the request.
Response structure: it should be in JSON format with the following fields: {"brand":"Asus","sub_model":"TUF Gaming","edition":"OC White","gpu_brand":"Nvidia","gpu_sup_brand":"GeForce","gpu_model":"RTX 5080","gpu_series":"RTX 5000","memory_size":8,"fans":2}
If the user did not specify a parameter, it is not included in the JSON.

Example:
    User: "GPU with 2 fans Asus RTX 4050TI with 24 video memory"
    Answer: {"brand":"Asus","gpu_model":"RTX 4050 TI","memory_size":24,"fans":2}

Example:
    User: "GTX 1660 super 8 gb memory two or more fans"
    Answer: {"gpu_model":"GTX 1660 super","memory_size":8,"fans":{">=", 2}}

Example:
    User: "I want a powerful graphics card with 16GB memory and a cooler"
    Answer: {"memory_size":16,"fans":{">=":1}}

Example:
    User: "Looking for a 3070 but needs to be fast and cool"
    Answer: {"gpu_model":"RTX 3070","fans":{">=":1}}

Example:
    User: "Need an Nvidia card with more than 10GB and less 20 of VRAM"
    Answer: {"gpu_brand":"Nvidia","memory_size":{">":10, "<":20}}

Example:
    User: "A good graphics card, maybe with a bit of overclocking, 8GB memory"
    Answer: {"memory_size":8,"edition":"OC"}

Example:
    User: "Anything with 8GB VRAM from Asus"
    Answer: {"brand":"Asus","memory_size":8}

Example:
    User: "Looking for a 4k capable card, not sure about model but with 12GB of memory"
    Answer: {"memory_size":12}
"""


cpu = {
    "brand": "AMD",
    "cores": 6,
    "threads": 12,
    "multithreading": False,
    "igp": True,
    "socket": "AM5",
    "approximate_name": "AMD Ryzen 5 Raphael 7500F OEM (100-000000597)",
}
# "Clock speed": "3.7 GHz",
# "TurboBoost / TurboCore": "5 GHz",

cpu_prompt = """

Example:
    User: "AMD processor with 6 cores, with integrated graphics"
    Answer: {"brand":"amd","cores":6,"igp":true}

Example:
    User: "12 core 16 thread with multithreading and no graphics card"
    Answer: {"cores":12,"threads": 16,"multithreading":false}

Example:
    User: "intel i5 10 generation with graphic"
    Answer: {"brand":"intel","igp":true,"approximate_name":"intel i5 10 generation"}

Example:
    User: "i9 intel core ultra without integrated gpu"
    Answer: {"brand":"intel","igp":false,"approximate_name":"i9 intel core ultra"}

Example:
    User: "Looking for an AMD Ryzen CPU, at least 8 cores, must have hyperthreading"
    Answer: {"brand":"AMD","cores":{">=":8},"multithreading":true,"approximate_name":"AMD Ryzen"}

Example:
    User: "Intel processor, no integrated graphics, LGA1700"
    Answer: {"brand":"Intel","igp":false,"socket":"LGA1700"}

Example:
    User: "I need a CPU with 6 cores and 12 threads, preferably AMD"
    Answer: {"brand":"AMD","cores":6,"threads":12}

Example:
    User: "Ryzen 7 with iGPU"
    Answer: {"igp":true,"approximate_name":"Ryzen 7"}

Example:
    User: "Something like an i7 12700K, but don't need integrated graphics"
    Answer: {"igp":false,"approximate_name":"i7 12700K"}

Example:
    User: "Best CPU for gaming, at least 6 cores, AM5 socket"
    Answer: {"cores":{">=":6},"socket":"AM5","approximate_name":"best gaming CPU"}

Example:
    User: "High-performance processor with multithreading, no integrated GPU"
    Answer: {"multithreading":true,"igp":false}

Example:
    User: "Ryzen 9, any model, AM4 socket, integrated graphics would be nice"
    Answer: {"socket":"AM4","igp":true,"approximate_name":"Ryzen 9"}

Example:
    User: "Intel Core Ultra, need 14 cores and multithreading"
    Answer: {"brand":"Intel","cores":14,"multithreading":true,"approximate_name":"Intel Core Ultra"}

Example:
    User: "10-core CPU, LGA1200, needs to have integrated graphics"
    Answer: {"cores":10,"socket":"LGA1200","igp":true}

"""


gpu = {
    "gpu_brand": "Asus",
    "gpu_mem_size": 8,
    "gpu_fans": 2,
    "gpu_model": "Asus GeForce RTX 5080 TUF Gaming OC White",  # for RAG
}


ram = {
    "ram_manufacturer": "Kingston Fury",
    "ram_mem_capacity": 32,
    "ram_mem_speed": 6000,
    "ram_type": "DDR5",
    #
    "ram_features": ["overclocking", "XMP", "EXPO"],
    #
    "ram_model": "Kingston Fury Renegade DDR4 Black 2x16Gb RGB",
}


mb = {
    "mb_manufacturer": "MSI",
    #
    "mb_form_factor": "micro-ATX",
    "mb_socket": "AMD AM5",
    "mb_DDR5": "4 slot(s)",
    "mb_chipset": "AMD B650",
    #
    # "mb_features": "gaming",
    #
    "mb_LED_lighting": False,
    "mb_M.2 connector": "2",
    # "mb_BIOS FlashBack": False,
}


# case = {
#     "Features": "gaming",
#     "Form factor": "Midi Tower",
#     "Mount": "vertical",
#     "Motherboard support": "ATX",
#     "Board placement": "vertical",
#     "Dimensions (HxWxD)": "453x235x450 mm",
#     "Material": "steel",

#     "Front panel": "lattice",
#     "Side panel window": "tempered glass",
#     "More features": "hidden wiringCPU cooling mount window",
#     "manufacturer": "Vinga",
# }
