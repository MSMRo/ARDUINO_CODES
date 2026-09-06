from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


# Library Schemas
class LibraryBase(BaseModel):
    name: str
    is_builtin: bool
    header_file: str
    purpose: str
    installation_guide: str
    documentation_url: Optional[str] = None


class LibraryRead(LibraryBase):
    id: int
    peripheral_id: int
    model_config = ConfigDict(from_attributes=True)


# Code Example Schemas
class CodeExampleBase(BaseModel):
    title: str
    category: str
    difficulty: str
    description: str
    code: str
    explanation: str
    circuit_notes: Optional[str] = None
    order_index: int = 0


class CodeExampleRead(CodeExampleBase):
    id: int
    peripheral_id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# Peripheral Detail Schemas
class PeripheralDetailBase(BaseModel):
    full_description: str
    architecture_role: str
    hardware_specs: str
    hardware_registers: str
    mega2560_pins: str
    requires_external_library: bool
    library_analysis: str


class PeripheralDetailRead(PeripheralDetailBase):
    id: int
    peripheral_id: int
    model_config = ConfigDict(from_attributes=True)


# Peripheral Master Schemas
class PeripheralBase(BaseModel):
    slug: str
    name: str
    category: str
    icon: str
    summary: str
    order_index: int = 0


class PeripheralListRead(PeripheralBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PeripheralFullRead(PeripheralBase):
    id: int
    details: Optional[PeripheralDetailRead] = None
    code_examples: List[CodeExampleRead] = []
    libraries: List[LibraryRead] = []
    model_config = ConfigDict(from_attributes=True)
