import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.factory import create_app
from app.settings import Settings


class TrustBoundaryTest(unittest.TestCase):
    def test_public_app_does_not_expose_private_routes(self) -> None:
        app = create_app(Settings(app_mode="public", database_url="postgresql://public"))
        paths = {route.path for route in app.routes}

        self.assertIn("/health", paths)
        self.assertIn("/api/public/capabilities", paths)
        self.assertNotIn("/api/private/capabilities", paths)

    def test_private_app_exposes_private_routes_only(self) -> None:
        app = create_app(Settings(app_mode="private", database_url="postgresql://private"))
        paths = {route.path for route in app.routes}

        self.assertIn("/health", paths)
        self.assertIn("/api/private/capabilities", paths)
        self.assertNotIn("/api/public/capabilities", paths)

    def test_health_reports_the_running_trust_zone(self) -> None:
        app = create_app(Settings(app_mode="public", database_url="postgresql://public"))

        response = TestClient(app).get("/health")

        self.assertEqual(200, response.status_code)
        self.assertEqual({"status": "ok", "mode": "public"}, response.json())

    def test_settings_reject_unknown_mode(self) -> None:
        with self.assertRaises(ValueError):
            Settings(app_mode="combined", database_url="postgresql://db")

    def test_public_entrypoint_rejects_private_mode(self) -> None:
        with patch.dict(
            os.environ,
            {"APP_MODE": "private", "DATABASE_URL": "postgresql://private"},
            clear=True,
        ):
            with self.assertRaises(RuntimeError):
                from app.entrypoints import public  # noqa: F401


if __name__ == "__main__":
    unittest.main()
