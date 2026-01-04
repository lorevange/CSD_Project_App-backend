from datetime import datetime
from typing import Optional

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


Rating = Annotated[int, Field(ge=0, le=5)]
Comment = Annotated[str, Field(min_length=1, max_length=1000)]


class ReviewBase(BaseModel):
    rating: Rating
    comment: Comment


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[Rating] = None
    comment: Optional[Comment] = None


class ReviewAuthorOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    photo: Optional[bytes] = None

    model_config = ConfigDict(from_attributes=True)


class ReviewOut(BaseModel):
    id: int
    doctor_id: int
    author_id: int
    author: ReviewAuthorOut
    rating: int
    comment: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
