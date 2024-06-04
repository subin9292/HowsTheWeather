from pydantic import BaseModel

class CommentBase(BaseModel):
    name: str
    comment: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True  # 여기서는 from_attributes가 아닌 orm_mode를 사용합니다.
