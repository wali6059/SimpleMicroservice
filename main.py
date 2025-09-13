from __future__ import annotations

import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.assignment import AssignmentCreate, AssignmentRead, AssignmentUpdate
from models.course import CourseCreate, CourseRead, CourseUpdate
from models.health import Health

port = int(8000)

assignments: Dict[UUID, AssignmentRead] = {}
courses: Dict[UUID, CourseRead] = {}

app = FastAPI()


def make_health(echo: Optional[str], path_echo: Optional[str] = None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo,
    )


@app.get("/health", response_model=Health)
def get_health_no_path(
    echo: str | None = Query(None, description="Optional echo string")
):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)


@app.get(
    "/health/{path_echo}",
    response_model=Health,
)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)


@app.post(
    "/assignments",
    response_model=AssignmentRead,
    status_code=201,
    tags=["assignments"],
    summary="Create a new assignment",
    description="Create a new assignment with the provided information",
)
def create_assignment(assignment: AssignmentCreate):
    assignment_read = AssignmentRead(**assignment.model_dump())
    assignments[assignment_read.id] = assignment_read
    return assignment_read


@app.get(
    "/assignments",
    response_model=List[AssignmentRead],
    tags=["assignments"],
    summary="List all assignments",
    description="Retrieve all assignments with optional filtering by course, dates, points, and other criteria",
)
def list_assignments(
    id: Optional[UUID] = Query(None, description="Filter by assignment ID"),
    course_id: Optional[UUID] = Query(None, description="Filter by course ID"),
    title: Optional[str] = Query(
        None, description="Filter by assignment title (partial match)"
    ),
    due_date_from: Optional[str] = Query(
        None, description="Filter assignments due from this date (YYYY-MM-DD)"
    ),
    due_date_to: Optional[str] = Query(
        None, description="Filter assignments due to this date (YYYY-MM-DD)"
    ),
    min_points: Optional[float] = Query(None, description="Minimum points possible"),
    max_points: Optional[float] = Query(None, description="Maximum points possible"),
    group_assignment: Optional[bool] = Query(
        None, description="Filter group assignments"
    ),
    late_submission_allowed: Optional[bool] = Query(
        None, description="Filter by late submission policy"
    ),
):
    results = list(assignments.values())
    if id is not None:
        results = [a for a in results if a.id == id]
    if course_id is not None:
        results = [a for a in results if a.course_id == course_id]
    if title is not None:
        results = [a for a in results if title.lower() in a.title.lower()]
    if due_date_from is not None:
        results = [
            a
            for a in results
            if a.due_date.date() >= datetime.fromisoformat(due_date_from).date()
        ]
    if due_date_to is not None:
        results = [
            a
            for a in results
            if a.due_date.date() <= datetime.fromisoformat(due_date_to).date()
        ]
    if min_points is not None:
        results = [a for a in results if float(a.points) >= min_points]
    if max_points is not None:
        results = [a for a in results if float(a.points) <= max_points]
    if group_assignment is not None:
        results = [a for a in results if a.group_assignment == group_assignment]
    if late_submission_allowed is not None:
        results = [
            a for a in results if a.late_submission_allowed == late_submission_allowed
        ]

    return results


@app.get(
    "/assignments/{assignment_id}",
    response_model=AssignmentRead,
    tags=["assignments"],
    summary="Get assignment by ID",
    description="Retrieve a specific assignment by its unique identifier",
)
def get_assignment(assignment_id: UUID):
    if assignment_id not in assignments:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignments[assignment_id]


@app.patch(
    "/assignments/{assignment_id}",
    response_model=AssignmentRead,
    tags=["assignments"],
    summary="Partially update assignment",
    description="Update specific fields of an existing assignment",
)
def update_assignment(assignment_id: UUID, update: AssignmentUpdate):
    if assignment_id not in assignments:
        raise HTTPException(status_code=404, detail="Assignment not found")
    stored = assignments[assignment_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    assignments[assignment_id] = AssignmentRead(**stored)
    return assignments[assignment_id]


@app.put(
    "/assignments/{assignment_id}",
    response_model=AssignmentRead,
    tags=["assignments"],
    summary="Replace entire assignment",
    description="Replace an entire assignment resource with new data",
)
def replace_assignment(assignment_id: UUID, assignment: AssignmentCreate):
    """Replace an entire assignment resource."""
    if assignment_id not in assignments:
        raise HTTPException(status_code=404, detail="Assignment not found")
    assignment_data = assignment.model_dump()
    assignment_data['id'] = assignment_id
    assignment_read = AssignmentRead(**assignment_data)
    assignments[assignment_id] = assignment_read
    return assignment_read


@app.delete(
    "/assignments/{assignment_id}",
    status_code=204,
    tags=["assignments"],
    summary="Delete assignment",
    description="Delete an assignment by its unique identifier",
)
def delete_assignment(assignment_id: UUID):
    """Delete an assignment by ID."""
    if assignment_id not in assignments:
        raise HTTPException(status_code=404, detail="Assignment not found")
    del assignments[assignment_id]


@app.post(
    "/courses",
    response_model=CourseRead,
    status_code=201,
    tags=["courses"],
    summary="Create a new course",
    description="Create a new course with the provided information",
)
def create_course(course: CourseCreate):
    course_read = CourseRead(**course.model_dump())
    courses[course_read.id] = course_read
    return course_read


@app.get(
    "/courses",
    response_model=List[CourseRead],
    tags=["courses"],
    summary="List all courses",
    description="Retrieve all courses with optional filtering by title, department, level, semester, year, and credits",
)
def list_courses(
    title: Optional[str] = Query(
        None, description="Filter by course title (partial match)"
    ),
    department: Optional[str] = Query(None, description="Filter by department"),
    level: Optional[int] = Query(None, description="Filter by course level"),
    semester: Optional[str] = Query(None, description="Filter by semester"),
    year: Optional[int] = Query(None, description="Filter by year"),
    min_credits: Optional[int] = Query(None, description="Minimum credit hours"),
    max_credits: Optional[int] = Query(None, description="Maximum credit hours"),
):
    results = list(courses.values())

    if title is not None:
        results = [c for c in results if title.lower() in c.title.lower()]
    if department is not None:
        results = [c for c in results if department.lower() in c.department.lower()]
    if level is not None:
        results = [c for c in results if c.level == level]
    if semester is not None:
        results = [c for c in results if c.semester == semester]
    if year is not None:
        results = [c for c in results if c.year == year]
    if min_credits is not None:
        results = [c for c in results if c.credits >= min_credits]
    if max_credits is not None:
        results = [c for c in results if c.credits <= max_credits]

    return results


@app.get(
    "/courses/{course_id}",
    response_model=CourseRead,
    tags=["courses"],
    summary="Get course by ID",
    description="Retrieve a specific course by its unique identifier",
)
def get_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]


@app.patch(
    "/courses/{course_id}",
    response_model=CourseRead,
    tags=["courses"],
    summary="Partially update course",
    description="Update specific fields of an existing course",
)
def update_course(course_id: UUID, update: CourseUpdate):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    stored = courses[course_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    courses[course_id] = CourseRead(**stored)
    return courses[course_id]


@app.put(
    "/courses/{course_id}",
    response_model=CourseRead,
    tags=["courses"],
    summary="Replace entire course",
    description="Replace an entire course resource with new data",
)
def replace_course(course_id: UUID, course: CourseCreate):
    """Replace an entire course resource."""
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    course_data = course.model_dump()
    course_data['id'] = course_id
    course_read = CourseRead(**course_data)
    courses[course_id] = course_read
    return course_read


@app.delete(
    "/courses/{course_id}",
    status_code=204,
    tags=["courses"],
    summary="Delete course",
    description="Delete a course by its unique identifier",
)
def delete_course(course_id: UUID):
    """Delete a course by ID."""
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    del courses[course_id]


@app.get("/")
def root():
    return {
        "message": "Welcome to the Course and Assignment Management API. See /docs for OpenAPI UI."
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
