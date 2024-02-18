import pydantic as _pydantic

# ------------------- USERS ------------------------

class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        # orm_mode = True
        from_attributes = True

class User(_UserBase):
    id: int

    class Config:
        # orm_mode = True
        from_attributes = True