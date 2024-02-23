from pydantic import BaseModel

# ------------------- USERS ------------------------
class UserBase(BaseModel):
    username: str
    password: str


# ------------------- ADMINS ------------------------
class AdminBase(BaseModel):
    username: str
    password: str
