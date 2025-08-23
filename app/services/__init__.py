from app.services.chat_service import ChatService
from app.services.component_service import (
    CpuService,
    GpuService,
    RamService,
    MotherboardService,
    PsuService,
)
from app.services.config_service import ConfigService
from app.services.user_service import UserService


chat_service = ChatService()
cpu_service = CpuService()
gpu_service = GpuService()
ram_service = RamService()
motherboard_service = MotherboardService()
psu_service = PsuService()
config_service = ConfigService()
user_service = UserService()


__all__ = (
    "chat_service",
    "cpu_service",
    "gpu_service",
    "ram_service",
    "motherboard_service",
    "psu_service",
    "config_service",
    "user_service",
)
