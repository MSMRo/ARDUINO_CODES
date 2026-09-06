import logging
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal, create_tables
from backend.app.models.peripheral import Peripheral, PeripheralDetail, CodeExample, Library
from backend.app.seed.seed_data import PERIPHERALS_DATA

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("seed")


def seed_database(db: Session = None, force: bool = False):
    """Populate database with ATmega2560 peripheral details, registers, and code examples."""
    should_close = False
    if db is None:
        create_tables()
        db = SessionLocal()
        should_close = True

    try:
        existing_count = db.query(Peripheral).count()
        if existing_count > 0 and not force:
            logger.info(f"Database already contains {existing_count} peripherals. Skipping seeding.")
            return

        if force and existing_count > 0:
            logger.info("Force re-seed requested. Clearing existing records...")
            db.query(Library).delete()
            db.query(CodeExample).delete()
            db.query(PeripheralDetail).delete()
            db.query(Peripheral).delete()
            db.commit()

        logger.info(f"Seeding {len(PERIPHERALS_DATA)} ATmega2560 hardware peripherals...")

        for p_data in PERIPHERALS_DATA:
            peripheral = Peripheral(
                slug=p_data["slug"],
                name=p_data["name"],
                category=p_data["category"],
                icon=p_data["icon"],
                summary=p_data["summary"],
                order_index=p_data["order_index"]
            )
            db.add(peripheral)
            db.flush()  # assign peripheral.id

            # Add Detail
            d_data = p_data.get("details", {})
            detail = PeripheralDetail(
                peripheral_id=peripheral.id,
                full_description=d_data.get("full_description", ""),
                architecture_role=d_data.get("architecture_role", ""),
                hardware_specs=d_data.get("hardware_specs", ""),
                hardware_registers=d_data.get("hardware_registers", ""),
                mega2560_pins=d_data.get("mega2560_pins", ""),
                requires_external_library=d_data.get("requires_external_library", False),
                library_analysis=d_data.get("library_analysis", "")
            )
            db.add(detail)

            # Add Libraries
            for lib_data in p_data.get("libraries", []):
                lib = Library(
                    peripheral_id=peripheral.id,
                    name=lib_data["name"],
                    is_builtin=lib_data.get("is_builtin", True),
                    header_file=lib_data["header_file"],
                    purpose=lib_data["purpose"],
                    installation_guide=lib_data["installation_guide"],
                    documentation_url=lib_data.get("documentation_url")
                )
                db.add(lib)

            # Add Code Examples
            for c_data in p_data.get("code_examples", []):
                code_ex = CodeExample(
                    peripheral_id=peripheral.id,
                    title=c_data["title"],
                    category=c_data.get("category", "Standard Arduino API"),
                    difficulty=c_data.get("difficulty", "Beginner"),
                    description=c_data["description"],
                    code=c_data["code"],
                    explanation=c_data["explanation"],
                    circuit_notes=c_data.get("circuit_notes"),
                    order_index=c_data.get("order_index", 0)
                )
                db.add(code_ex)

        db.commit()
        logger.info("Database seeding completed successfully!")
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    seed_database(force=True)
