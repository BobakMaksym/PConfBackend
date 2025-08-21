from fastapi import status as s
from fastapi.exceptions import HTTPException


ConfigDoesNotExistException = HTTPException(
    status_code=s.HTTP_404_NOT_FOUND, detail="The configuration does not exist"
)


UsernameIsAlreadyInUseException = HTTPException(
    status_code=s.HTTP_409_CONFLICT, detail="This username is already in use"
)

EmailIsAlreadyInUseException = HTTPException(
    status_code=s.HTTP_409_CONFLICT, detail="This email address is already in use"
)


UserDoesNotExistException = HTTPException(
    status_code=s.HTTP_404_NOT_FOUND, detail="User does not exist"
)


class DocumentDoesNotExist(Exception):
    def __init__(self):
        super().__init__("Document does not exist")
