class ValuesMixin:
    @classmethod
    def values(cls) -> list[str]:
        return [val.value for val in cls]  # type: ignore
