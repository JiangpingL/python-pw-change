from pydantic import BaseModel
from models.target_server import TargetServer

#
# model used for request validation
#
class TargetApplication(BaseModel):
    name: str
    port: int | None = None
    target_server: TargetServer