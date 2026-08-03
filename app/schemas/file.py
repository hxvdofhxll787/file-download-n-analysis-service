from pydantic import BaseModel

class FileNamesResponse(BaseModel):
    names: list[str]