from pydantic import BaseModel


class CreateEbook(BaseModel):
    topic: str
    target_audience: str
