import logging

from app.rules_engine.core import RuleInterface


logger = logging.getLogger("app")


class CompatibilityManager:
    def __init__(self):
        self.rules: list[RuleInterface] = []

    def add_rule(self, rule: RuleInterface):
        self.rules.append(rule)

    def check_compatibility(self, build):
        """checks the compatibility of the new component with the list of selected
        `through all added rules`"""

        errors: list[str] = []
        for rule in self.rules:
            errors.extend(rule.validate(build))

        logger.debug("Configuration %s errors: %s", build.id, errors)
        return errors


rule_manager = CompatibilityManager()
