from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal


class AssignmentBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Unique assignment identifier",
        json_schema_extra={"example": "11111111-1111-4111-8111-111111111111"},
    )
    course_id: UUID = Field(
        description="Reference to the course this assignment belongs to.",
        json_schema_extra={"example": "11111111-1111-4111-8111-111111111111"},
    )
    title: str = Field(
        description="Assignment title.",
        json_schema_extra={"example": "Introduction to Python Programming"},
    )
    description: str = Field(
        description="Detailed assignment description and requirements.",
        json_schema_extra={
            "example": "Complete a Python program that demonstrates basic programming concepts."
        },
    )
    points: Decimal = Field(
        description="Maximum points that can be earned.",
        json_schema_extra={"example": "100.0"},
    )
    due_date: datetime = Field(
        description="Assignment due date and time.",
        json_schema_extra={"example": "2024-02-15T23:59:59Z"},
    )
    late_submission_allowed: bool = Field(
        default=True,
        description="Whether late submissions are accepted.",
        json_schema_extra={"example": True},
    )
    group_assignment: bool = Field(
        default=False,
        description="Whether this is a group assignment.",
        json_schema_extra={"example": False},
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "21111111-1111-4111-8111-111111111111",
                    "course_id": "11111111-1111-4111-8111-111111111111",
                    "title": "Introduction to Python Programming",
                    "description": "Complete a Python program that demonstrates basic programming",
                    "points": "100.0",
                    "due_date": "2024-02-15T23:59:59Z",
                    "late_submission_allowed": True,
                    "group_assignment": False,
                }
            ]
        }
    }


class AssignmentCreate(AssignmentBase):
    """Creation payload for an Assignment."""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "course_id": "11111111-1111-4111-8111-111111111111",
                    "title": "Calculus Quiz",
                    "description": "Quiz covering integration by parts.",
                    "points": "50.0",
                    "due_date": "2024-03-20T15:30:00Z",
                    "late_submission_allowed": False,
                    "group_assignment": False,
                }
            ]
        }
    }


class AssignmentUpdate(BaseModel):
    """Partial update for an Assignment; supply only fields to change."""

    title: Optional[str] = Field(
        None, json_schema_extra={"example": "Updated Assignment Title"}
    )
    description: Optional[str] = Field(
        None, json_schema_extra={"example": "Updated description."}
    )
    points: Optional[Decimal] = Field(None, json_schema_extra={"example": "150.0"})
    due_date: Optional[datetime] = Field(
        None, json_schema_extra={"example": "2024-03-01T23:59:59Z"}
    )
    late_submission_allowed: Optional[bool] = Field(
        None, json_schema_extra={"example": False}
    )
    group_assignment: Optional[bool] = Field(None, json_schema_extra={"example": True})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"title": "Updated Assignment Title", "points": "150.0"},
                {"due_date": "2024-03-01T23:59:59Z", "late_submission_allowed": False},
                {"group_assignment": True},
            ]
        }
    }


class AssignmentRead(AssignmentBase):
    """Server representation returned to clients."""

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2024-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2024-02-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "33333333-3333-4333-8333-333333333333",
                    "course_id": "11111111-1111-4111-8111-145111111111",
                    "title": "Introduction to Python Programming",
                    "description": "Complete a Python program that demonstrates basic programming.",
                    "points": "100.0",
                    "due_date": "2024-02-15T23:59:59Z",
                    "late_submission_allowed": True,
                    "group_assignment": False,
                    "created_at": "2024-01-15T10:20:30Z",
                    "updated_at": "2024-02-16T12:00:00Z",
                }
            ]
        }
    }
