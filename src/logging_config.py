"""Central logging configuration for media_puller.

The :func:`setup_logging` function configures the root logger used
throughout the application. Modules should import this function and call
it once at application start-up.
"""
from __future__ import annotations

import logging
from typing import Optional


def setup_logging(level: int = logging.INFO) -> None:
    """Configure basic logging for the application.

    Parameters
    ----------
    level: int, optional
        Logging level for the root logger. Defaults to ``logging.INFO``.

    Side Effects
    ------------
    Initializes logging configuration for the running process.
    """
    if logging.getLogger().handlers:
        return
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
