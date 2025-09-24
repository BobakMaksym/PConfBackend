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
from app.core.configs.typesense_config import get_client
from app.repos.index_repo import SearchIndexRepo


search_index = SearchIndexRepo(client=get_client())


chat_service = ChatService()
cpu_service = CpuService(index=search_index)
gpu_service = GpuService(index=search_index)
ram_service = RamService(index=search_index)
motherboard_service = MotherboardService(index=search_index)
psu_service = PsuService(index=search_index)
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
