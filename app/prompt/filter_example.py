FILTER_EXAMPLES = [
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
        "Response": {},
    },
]
