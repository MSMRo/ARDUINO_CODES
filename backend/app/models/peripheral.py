from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.core.database import Base


class Peripheral(Base):
    """
    Table 1: contents of peripherals (Master list of ATmega2560 hardware modules)
    """
    __tablename__ = "peripherals"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # Serial, Timers & PWM, Analog, Digital, Core
    icon = Column(String(20), default="🔌")
    summary = Column(Text, nullable=False)
    order_index = Column(Integer, default=0)

    # Relationships
    details = relationship("PeripheralDetail", back_populates="peripheral", uselist=False, cascade="all, delete-orphan")
    code_examples = relationship("CodeExample", back_populates="peripheral", cascade="all, delete-orphan", order_by="CodeExample.order_index")
    libraries = relationship("Library", back_populates="peripheral", cascade="all, delete-orphan")


class PeripheralDetail(Base):
    """
    Table 2: detailed description, registers, pinouts, and library requirements
    """
    __tablename__ = "peripheral_details"

    id = Column(Integer, primary_key=True, index=True)
    peripheral_id = Column(Integer, ForeignKey("peripherals.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    full_description = Column(Text, nullable=False)
    architecture_role = Column(Text, nullable=False)
    hardware_specs = Column(Text, nullable=False)       # JSON or formatted markdown
    hardware_registers = Column(Text, nullable=False)   # Register table / details
    mega2560_pins = Column(Text, nullable=False)        # Pinout mapping on Mega 2560
    requires_external_library = Column(Boolean, default=False)
    library_analysis = Column(Text, nullable=False)     # Detailed guidance on whether libraries are needed

    peripheral = relationship("Peripheral", back_populates="details")


class CodeExample(Base):
    """
    Table 3: Arduino code examples, from beginner to bare-metal AVR registers
    """
    __tablename__ = "code_examples"

    id = Column(Integer, primary_key=True, index=True)
    peripheral_id = Column(Integer, ForeignKey("peripherals.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)  # e.g., 'Arduino API', 'Direct Register (AVR C++)', 'Library'
    difficulty = Column(String(20), default="Beginner")  # Beginner, Intermediate, Advanced
    description = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    circuit_notes = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    peripheral = relationship("Peripheral", back_populates="code_examples")


class Library(Base):
    """
    Table 4: Associated Arduino & AVR libraries
    """
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, index=True)
    peripheral_id = Column(Integer, ForeignKey("peripherals.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String(100), nullable=False)
    is_builtin = Column(Boolean, default=True)  # True = bundled in Arduino IDE, False = 3rd party
    header_file = Column(String(50), nullable=False)  # e.g. <Wire.h>, <SPI.h>, <avr/wdt.h>
    purpose = Column(Text, nullable=False)
    installation_guide = Column(Text, nullable=False)
    documentation_url = Column(String(255), nullable=True)

    peripheral = relationship("Peripheral", back_populates="libraries")
