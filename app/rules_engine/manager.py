from app.rules_engine.rules import (
    SocketCompatibility,
    RamTypeMatches,
    PsuPowerSufficiency,
)
from app.rules_engine._manager import rule_manager


rule_manager.add_rule(SocketCompatibility)
rule_manager.add_rule(RamTypeMatches)
rule_manager.add_rule(PsuPowerSufficiency)
