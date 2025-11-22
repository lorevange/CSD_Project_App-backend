from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    first_name: str
    last_name: str
    identity_number: str
    profile: str
    email: str
    phone_number: str | None = None


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
