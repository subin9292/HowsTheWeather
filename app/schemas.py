from pydantic import BaseModel

class CommentBase(BaseModel):
    name: str
    comment: str
    region: str  # 새로운 필드 추가

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic V2 설정
