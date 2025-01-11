class BaseCompatibilityException(Exception):
    """Base Class for compatibility errors"""

    message = None

    def __init__(self, message: str, *args):
        super().__init__(message)
        self.message = message
        self.values = args

    def __str__(self):
        return f"{self.message}.\n    Value: {self.values}"

    def __reduce__(self):
        return self.__class__, (self.message, *self.values)


class CompatibilityException(BaseCompatibilityException):
    """Class for common compatibility errors.
    Adds the prefix “Compatibility error: ” to the message
    """

    def __str__(self):
        return f"Compatibility error: {self.message}.\n    Value: {self.values}"


class SocketCompatibilityException(CompatibilityException):
    def __init__(self, *args):
        super().__init__("Incompatible sockets", *args)


class RamTypeCompatibilityException(CompatibilityException):
    def __init__(self, *args):
        super().__init__("Incompatible ram type", *args)


if __name__ == "__main__":
    from dataclasses import dataclass

    @dataclass
    class MotherBoard:
        socket: str

    @dataclass
    class CPU:
        socket: str

    mb = MotherBoard("am4")
    cpu = MotherBoard("am5")

    ex = BaseCompatibilityException("Incompatible components", mb.socket, cpu.socket)
    print(ex)
    ex = CompatibilityException("Incompatible type", mb.socket, cpu.socket)
    print(ex)
    ex = SocketCompatibilityException(mb.socket, cpu.socket)
    print(ex)
