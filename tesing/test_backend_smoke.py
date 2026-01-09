import os
import sys
import unittest
import tempfile
from datetime import timedelta
import importlib
from pathlib import Path
from unittest import mock


# Ensure backend modules are importable.
# The backend code lives in "backend-visionguard-ai/" and uses the top-level package "app".
REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = REPO_ROOT / "backend-visionguard-ai"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


def require_module(module_name: str) -> None:
    """Skip the current test if an optional dependency isn't installed."""

    try:
        importlib.import_module(module_name)
    except ImportError as exc:
        raise unittest.SkipTest(f"Missing dependency: {module_name}") from exc


class TestAuthUtilities(unittest.TestCase):
    def test_password_hash_and_verify(self):
        require_module("passlib")
        require_module("jwt")
        from app.core.auth import hash_password, verify_password

        password = "CorrectHorseBatteryStaple!"
        hashed = hash_password(password)

        self.assertIsInstance(hashed, str)
        self.assertNotEqual(hashed, password)
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("wrong", hashed))

    def test_jwt_roundtrip(self):
        require_module("passlib")
        require_module("jwt")
        os.environ["JWT_SECRET_KEY"] = "test-secret"

        from app.core import auth as auth_mod

        payload = {"sub": "123", "email": "a@b.com", "role": "owner"}
        token = auth_mod.create_access_token(payload, expires_delta=timedelta(minutes=5))
        decoded = auth_mod.verify_token(token)

        self.assertIsInstance(decoded, dict)
        self.assertEqual(decoded.get("sub"), "123")
        self.assertEqual(decoded.get("email"), "a@b.com")
        self.assertEqual(decoded.get("role"), "owner")

    def test_expired_token_is_rejected(self):
        require_module("passlib")
        require_module("jwt")
        os.environ["JWT_SECRET_KEY"] = "test-secret"

        from app.core import auth as auth_mod

        payload = {"sub": "123"}
        token = auth_mod.create_access_token(payload, expires_delta=timedelta(seconds=-1))
        decoded = auth_mod.verify_token(token)

        self.assertIsNone(decoded)


class TestConfigUtilities(unittest.TestCase):
    def test_resolve_device_cuda_fallback(self):
        require_module("torch")
        from app import config as cfg

        with mock.patch.object(cfg.torch.cuda, "is_available", return_value=False):
            self.assertEqual(cfg.resolve_device("cuda:0"), "cpu")
            self.assertEqual(cfg.resolve_device("gpu"), "cpu")


class TestAnomalyService(unittest.TestCase):
    def test_determine_severity_mapping(self):
        require_module("cv2")
        require_module("numpy")
        from app.services.anomaly_service import AnomalyService
        from app.models.anomaly import AnomalySeverity

        self.assertEqual(AnomalyService.determine_severity("High", 999), AnomalySeverity.HIGH)
        self.assertEqual(AnomalyService.determine_severity("Medium", 1.0), AnomalySeverity.MEDIUM)
        self.assertEqual(AnomalyService.determine_severity("Low", 0.1), AnomalySeverity.LOW)
        # Default branch
        self.assertEqual(AnomalyService.determine_severity("Unknown", 0.1), AnomalySeverity.LOW)

    def test_save_frame_writes_file(self):
        require_module("cv2")
        require_module("numpy")
        import numpy as np

        from app.services import anomaly_service as anomaly_mod
        from app.services.anomaly_service import AnomalyService

        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch.object(anomaly_mod, "ANOMALY_FRAMES_DIR", tmpdir):
                frame = np.zeros((64, 64, 3), dtype=np.uint8)
                from datetime import datetime

                rel_path = AnomalyService.save_frame(frame, shop_id="shop-1", timestamp=datetime.utcnow())

                self.assertIsInstance(rel_path, str)
                abs_path = os.path.join(tmpdir, rel_path)
                self.assertTrue(os.path.exists(abs_path))


if __name__ == "__main__":
    unittest.main(verbosity=2)
