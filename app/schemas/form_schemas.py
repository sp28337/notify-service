from pydantic import BaseModel


class ShortFormSchema(BaseModel):
    name: str
    phone: str
