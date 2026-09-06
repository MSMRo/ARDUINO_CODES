from backend.app.controllers.peripheral_controller import router as peripheral_router
from backend.app.controllers.code_controller import router as code_router
from backend.app.controllers.health_controller import router as health_router

__all__ = ["peripheral_router", "code_router", "health_router"]
