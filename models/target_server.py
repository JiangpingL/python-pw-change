from pydantic import BaseModel

#
# model used for request validation
#
class TargetServer(BaseModel):
    host: str
