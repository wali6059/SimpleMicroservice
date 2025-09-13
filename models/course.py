from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Course identifier.",
        json_schema_extra={"example": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"},
    )
    title: str = Field(
        description="Course title.",
        json_schema_extra={"example": "Introduction to Computer Science"},
    )
    description: Optional[str] = Field(
        None,
        description="Detailed course description.",
        json_schema_extra={
            "example": "An introduction to computer science concepts including programming fundamentals, data structures, and algorithms."
        },
    )
    credits: int = Field(
        description="Number of credit hours (typically 1-6).",
        json_schema_extra={"example": 3},
    )
    department: str = Field(
        description="Academic department offering the course.",
        json_schema_extra={"example": "Computer Science"},
    )
    level: int = Field(
        description="Course level (1000, 2000, 3000, 4000).",
        json_schema_extra={"example": 1000},
    )
    semester: str = Field(
        description="Semester when the course is offered.",
        json_schema_extra={"example": "fall"},
    )
    year: int = Field(
        description="Academic year.",
        json_schema_extra={"example": 2024},
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "13411111-1111-4111-8111-111111111111",
                    "title": "Introduction to Databases",
                    "description": "An introduction to database concepts.",
                    "credits": 3,
                    "department": "Computer Science",
                    "level": 3000,
                    "semester": "fall",
                    "year": 2024,
                }
            ]
        }
    }


class CourseCreate(CourseBase):
    """Creation payload for a Course."""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Calculus II",
                    "description": "Continuation of calculus concepts including integration techniques, series, and differential equations.",
                    "credits": 4,
                    "department": "Mathematics",
                    "level": 2000,
                    "semester": "spring",
                    "year": 2024,
                }
            ]
        }
    }


class CourseUpdate(BaseModel):
    """Partial update for a Course; supply only fields to change."""

    title: Optional[str] = Field(
        None, json_schema_extra={"example": "Advanced Computer Science"}
    )
    description: Optional[str] = Field(
        None, json_schema_extra={"example": "Updated course description."}
    )
    credits: Optional[int] = Field(None, json_schema_extra={"example": 4})
    department: Optional[str] = Field(
        None, json_schema_extra={"example": "Mathematics"}
    )
    level: Optional[int] = Field(None, json_schema_extra={"example": 3000})
    semester: Optional[str] = Field(None, json_schema_extra={"example": "spring"})
    year: Optional[int] = Field(None, json_schema_extra={"example": 2025})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"title": "Advanced Computer Science", "level": 3000},
                {"credits": 4, "department": "Mathematics"},
                {"semester": "spring", "year": 2025},
            ]
        }
    }


class CourseRead(CourseBase):
    """Server representation returned to clients."""

    created_at: datetime = Field(
        default_factory=datetime,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2024-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2024-02-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "22222222-2222-4222-8222-222222222222",
                    "title": "Introduction to Computer Science",
                    "description": "An introduction to computer science concepts including programming fundamentals, data structures, and algorithms.",
                    "credits": 3,
                    "department": "Computer Science",
                    "level": 1000,
                    "semester": "fall",
                    "year": 2024,
                    "created_at": "2024-01-15T10:20:30Z",
                    "updated_at": "2024-02-16T12:00:00Z",
                }
            ]
        }
    }

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "22222222-2222-4222-8222-222222222222",
                    "title": "Introduction to Computer Science",
                    "description": "An introduction to computer science concepts including programming fundamentals, data structures, and algorithms.",
                    "credits": 3,
                    "department": "Computer Science",
                    "level": 1000,
                    "semester": "fall",
                    "year": 2024,
                    "created_at": "2024-01-15T10:20:30Z",
                    "updated_at": "2024-02-16T12:00:00Z",
                }
            ]
        }
    }
