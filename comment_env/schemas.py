from pydantic import BaseModel

class CommentBase(BaseModel):
    name: str
    comment: str
    region: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True
