from fastapi import status
from fastapi.exceptions import HTTPException


ConfigDoesNotExistException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="The configuration does not exist"
)


class DocumentDoesNotExist(Exception):
    def __init__(self):
        super().__init__("Document does not exist")
