from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.core.database import get_db
from backend.app.models.peripheral import CodeExample
from backend.app.schemas.peripheral import CodeExampleRead

router = APIRouter(prefix="/codes", tags=["Code Examples"])


@router.get("", response_model=List[CodeExampleRead], summary="Search code examples")
def search_code_examples(
    q: Optional[str] = Query(None, description="Search keyword in title, code, or description"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty (Beginner, Intermediate, Advanced)"),
    db: Session = Depends(get_db)
):
    """Search and filter Arduino code examples across all peripherals."""
    query = db.query(CodeExample)
    if difficulty:
        query = query.filter(CodeExample.difficulty.ilike(difficulty))
    if q:
        search_pattern = f"%{q}%"
        query = query.filter(
            or_(
                CodeExample.title.ilike(search_pattern),
                CodeExample.description.ilike(search_pattern),
                CodeExample.code.ilike(search_pattern),
                CodeExample.explanation.ilike(search_pattern)
            )
        )
    return query.order_by(CodeExample.order_index).all()


@router.get("/{code_id}", response_model=CodeExampleRead, summary="Get code example by ID")
def get_code_example(code_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific code example with commentary and circuit notes."""
    code = db.query(CodeExample).filter(CodeExample.id == code_id).first()
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Code example with ID {code_id} not found."
        )
    return code
