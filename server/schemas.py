from pydantic import BaseModel

# ------------------- USERS ------------------------
class UserBase(BaseModel):
    username: str
    password: str


# class UserCreate(UserBase):
#     hashed_password: str

#     class Config:
#         from_attributes = True

# class User(UserBase):
#     id: int

#     class Config:
#         from_attributes = True