"""Public VoxVane client. It only calls the HTTP API and only returns audio bytes."""

from .client import VoxVane, VoxVaneError

__all__ = ["VoxVane", "VoxVaneError"]
__version__ = "0.1.0"
