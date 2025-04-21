{
    "client_id": "string",  # унікальний ідентифікатор
    "raw_text": "string",  # оригінальний текст запиту
    "filters": {
        "pc_type": ["office", "gaming"],  # тип/сценарії використання
        "programs": ["MS Word", "games"],
        "budget": {"currency": "UAH", "<=": 30000, ">=": 15000},
        #
        "cpu": {
            "manufacturer": "intel",
            "model": "i5-12400F",
            "cores": {">=": 6, "<=": 8},
            "threads": {">=": 12},
        },
        "gpu": {
            "manufacturer": "nvidia",  # "nvidia" | "amd"
            "model": "RTX 3060",
            "memory": {">=": 6, "<=": 24},
            "color": "white",
            "features": ["ray_tracing", "nvenc"],
        },
        "ram": {
            "manufacturer": "samsung",
            "model": "...",
            "type": "DDR4",  # "DDR4" | "DDR5"
            "memory": {"=": 16},
            "modules": 2,
            "speed": {">=": 3200},
            "color": "white",
        },
        "storage": [
            {
                "type": "SSD",  # "SSD" | "HDD"
                "interface": "NVMe",  # "NVMe" | "SATA"
                "memory": {">=": 500},
            }
        ],
        "motherboard": {
            "socket": "LGA1700",
            "form_factor": ["ATX", "mATX"],
            "ram_slots": {">=": 2},
        },
        "psu": {"wattage": {">=": 500}, "efficiency": "80+ Gold", "modular": True},
        "case": {
            "form_factor": "ITX",  # "ATX" | "mATX" | "ITX"
            "noise_preference": "low",  # "low" | "medium" | "high"
        },
        "cooling": {"type": "air", "radiator_size": 240},  # "air" | "liquid"
        "constraints": {
            "linux_compatible": True,
            "max_noise_db": {"<=": 30},
            "max_size_mm": {"height": {"<=": 400}, "depth": {"<=": 400}},
        },
    },
}


##########################################################################################


schema_metadata = {
    "customers": {
        "columns": ["id", "name", "email", "country"],
        "description": "Stores customer details",
    },
    "orders": {
        "columns": ["id", "customer_id", "product_id", "quantity", "order_date"],
        "description": "Tracks customer orders",
    },
}


user_query = "Show me all customers who placed an order in the last 30 days"


relevant_tables = ["customers", "orders"]
schema_context = {table: schema_metadata[table] for table in relevant_tables}


prompt = f"""
User query: {user_query}
Relevant schema details:
{schema_context}
Please generate an SQL query using the provided schema.
"""
