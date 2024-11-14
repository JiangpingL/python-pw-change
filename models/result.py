from pydantic import BaseModel

#
# model used for response validation
#
class Result(BaseModel):
    success: bool
    message: str