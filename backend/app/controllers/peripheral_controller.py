from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.peripheral import Peripheral
from backend.app.schemas.peripheral import PeripheralListRead, PeripheralFullRead

router = APIRouter(prefix="/peripherals", tags=["Peripherals"])


@router.get("", response_model=List[PeripheralListRead], summary="List all ATmega2560 peripherals")
def list_peripherals(db: Session = Depends(get_db)):
    """Retrieve all available ATmega2560 peripherals ordered by order_index."""
    return db.query(Peripheral).order_by(Peripheral.order_index).all()


@router.get("/categories", response_model=List[str], summary="List peripheral categories")
def list_categories(db: Session = Depends(get_db)):
    """Retrieve distinct categories for sidebar navigation grouping."""
    results = db.query(Peripheral.category).distinct().order_by(Peripheral.category).all()
    return [r[0] for r in results if r[0]]


@router.get("/{slug_or_id}", response_model=PeripheralFullRead, summary="Get full peripheral details and codes")
def get_peripheral(slug_or_id: str, db: Session = Depends(get_db)):
    """Retrieve full details, registers, pinouts, libraries, and code examples for a peripheral by slug or ID."""
    query = db.query(Peripheral)
    if slug_or_id.isdigit():
        peripheral = query.filter(Peripheral.id == int(slug_or_id)).first()
    else:
        peripheral = query.filter(Peripheral.slug == slug_or_id.lower()).first()

    if not peripheral:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Peripheral '{slug_or_id}' not found."
        )
    return peripheral
