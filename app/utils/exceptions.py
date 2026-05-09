from fastapi import HTTPException


class BadRequest(HTTPException):
    def __init__(self, detail: str | dict = "Bad request"):
        super().__init__(status_code=400, detail=detail)