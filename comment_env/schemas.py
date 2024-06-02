from pydantic import BaseModel

class CommentBase(BaseModel):
    name: str
    comment: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2에서는 'orm_mode'가 'from_attributes'로 변경되었습니다.
