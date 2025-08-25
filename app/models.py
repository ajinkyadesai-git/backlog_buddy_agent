from pydantic import BaseModel, Field, conlist
from typing import List

class StoryModel(BaseModel):
    story_title: str = Field(..., min_length=3, max_length=180)
    user_story: str
    acceptance_criteria: conlist(str, min_length=2)
    labels: List[str] = []
    estimate_points: int = 1
