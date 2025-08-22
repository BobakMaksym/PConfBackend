from app.db import db
from app.repos.chat_repo import ChatRepo
from app.repos.component_repo import (
    CpuRepo,
    GpuRepo,
    RamRepo,
    MbRepo,
    PsuRepo,
)
from app.repos.config_repo import ConfigRepo
from app.repos.user_repo import UserRepo


chat_repo = ChatRepo(db)
cpu_repo = CpuRepo(db)
gpu_repo = GpuRepo(db)
ram_repo = RamRepo(db)
mb_repo = MbRepo(db)
psu_repo = PsuRepo(db)
config_repo = ConfigRepo(db)
user_repo = UserRepo(db)


__all__ = (
    "chat_repo",
    "cpu_repo",
    "gpu_repo",
    "ram_repo",
    "mb_repo",
    "psu_repo",
    "config_repo",
    "user_repo",
)
