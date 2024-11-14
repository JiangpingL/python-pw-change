from typing import ForwardRef
from pydantic import BaseModel
from models.target_application import TargetApplication

TargetAccount = ForwardRef('TargetAccount')

#
# model used for request validation
#
class TargetAccount(BaseModel):
    name: str
    password: str
    new_password: str | None = None
    master_account: TargetAccount | None = None
    target_application: TargetApplication