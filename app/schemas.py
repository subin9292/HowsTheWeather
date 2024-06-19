from pydantic import BaseModel

class CommentBase(BaseModel):
    name: str
    comment: str
    lat: float
    lon: float

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True
