from pymongo.errors import DuplicateKeyError


class UsernameDuplicateError(DuplicateKeyError):
    def __init__(self):
        super().__init__(error="This username is already in use")


class EmailDuplicateError(DuplicateKeyError):
    def __init__(self):
        super().__init__(error="This email is already in use")
