from pydantic import BaseModel, Field

class BaseDataPushSchemas(BaseModel):
    to: str
    subject: str
    message: str
