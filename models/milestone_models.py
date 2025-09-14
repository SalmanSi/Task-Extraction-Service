# models/milestone_models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class Task(BaseModel):
    title: str = Field(description="Title of the milestone/task")
    description: str = Field(description="A detailed description of the task, as mentioned in the document")
    deliverable: str = Field(description="A brief definition of done / deliverable of the milestone")
    due_date: str = Field(description="Due date / deadline of the task as mentioned in the document in the format YYYY-MM-DD")

class MilestoneExtractionResult(BaseModel):
    status: str = Field(
        description="The status of the milestone extraction by the LLM.\"success\" if milestones were extracted, otherwise \"failed\"."
    )
    tasks: Optional[List[Task]] = Field(
        default=None,
        description="The list of extracted tasks/milestones if status is \"success\"; otherwise None."
    )
    message: Optional[str] = Field(
        default="",
        description="If status is \"failed\", this explains why milestone extraction failed. If status is \"success\", this should be an empty string."
    )

