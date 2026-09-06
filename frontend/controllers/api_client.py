import os
import requests
from typing import List, Dict, Any, Optional

FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://127.0.0.1:8000")
API_V1 = f"{FASTAPI_BASE_URL}/api/v1"


class ArduinoAPIClient:
    """
    Frontend Controller: Communicates with FastAPI backend REST endpoints.
    Provides fallback to local seed data if backend is offline.
    """

    def __init__(self, base_url: str = API_V1, timeout: float = 3.0):
        self.base_url = base_url
        self.timeout = timeout

    def check_health(self) -> Dict[str, Any]:
        """Check status of backend API and database."""
        try:
            r = requests.get(f"{FASTAPI_BASE_URL}/health", timeout=self.timeout)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            return {
                "status": "offline",
                "message": f"Backend unreachable ({e})",
                "database": {"status": "offline", "engine_dialect": "none"},
                "stats": {"total_peripherals": 10, "total_code_examples": 15}
            }
        return {"status": "unknown"}

    def get_peripherals(self) -> List[Dict[str, Any]]:
        """Fetch all peripherals."""
        try:
            r = requests.get(f"{self.base_url}/peripherals", timeout=self.timeout)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        # Fallback to local data
        return self._get_fallback_peripherals()

    def get_peripheral_detail(self, slug: str) -> Optional[Dict[str, Any]]:
        """Fetch complete details, registers, libraries, and code examples for a peripheral."""
        try:
            r = requests.get(f"{self.base_url}/peripherals/{slug}", timeout=self.timeout)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        # Fallback
        return self._get_fallback_detail(slug)

    def search_codes(self, query: str = "", difficulty: str = "") -> List[Dict[str, Any]]:
        """Search code examples."""
        try:
            params = {}
            if query:
                params["q"] = query
            if difficulty:
                params["difficulty"] = difficulty
            r = requests.get(f"{self.base_url}/codes", params=params, timeout=self.timeout)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return []

    # Internal fallback mechanism
    def _get_fallback_peripherals(self) -> List[Dict[str, Any]]:
        try:
            from backend.app.seed.seed_data import PERIPHERALS_DATA
            return [
                {
                    "id": idx + 1,
                    "slug": p["slug"],
                    "name": p["name"],
                    "category": p["category"],
                    "icon": p["icon"],
                    "summary": p["summary"],
                    "order_index": p["order_index"]
                }
                for idx, p in enumerate(PERIPHERALS_DATA)
            ]
        except Exception:
            return []

    def _get_fallback_detail(self, slug: str) -> Optional[Dict[str, Any]]:
        try:
            from backend.app.seed.seed_data import PERIPHERALS_DATA
            for idx, p in enumerate(PERIPHERALS_DATA):
                if p["slug"] == slug:
                    return {
                        "id": idx + 1,
                        "slug": p["slug"],
                        "name": p["name"],
                        "category": p["category"],
                        "icon": p["icon"],
                        "summary": p["summary"],
                        "order_index": p["order_index"],
                        "details": p.get("details", {}),
                        "libraries": p.get("libraries", []),
                        "code_examples": p.get("code_examples", [])
                    }
        except Exception:
            pass
        return None


api_client = ArduinoAPIClient()
