import logging

from agents import RunContextWrapper

from app.schemas.pc_config_schema import PcConfigContext


logger = logging.getLogger("app")


def on_handoff_configurator(ctx: RunContextWrapper[PcConfigContext]):
    logger.info("Спрацював агент конфігуратор")
    logger.info("context: %s", ctx)


def on_handoff_questioner(ctx: RunContextWrapper[PcConfigContext]):
    logger.info("Спрацював агент questioner")
    logger.info("context: %s", ctx)
