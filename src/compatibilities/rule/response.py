from dataclasses import dataclass, field


@dataclass
class CompRuleResponse:
    """Результат перевірки сумісності."""

    compatible: bool
    errors: dict[str, str] = field(default_factory=dict)

    def __repr__(self):
        return f"CompRuleResponse({self.compatible}, {self.errors})"
