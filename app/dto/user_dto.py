from pydantic import BaseModel, Field, ConfigDict


class UserCreateDTO(BaseModel):
    email: str = Field()
    password: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    phone: str | None = Field(None)


class UserUpdateDTO(BaseModel):
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    phone: str | None = Field(None)


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field()
    email: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    phone: str | None = Field()


class UserListDTO(BaseModel):
    items: list[UserDTO] = Field()
    total: int = Field()
