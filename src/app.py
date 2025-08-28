"""Application entry point for media_puller."""
from __future__ import annotations

import logging

from .gui import DownloaderGUI
from .logging_config import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the GUI application.

    Returns
    -------
    None

    Side Effects
    ------------
    Configures logging and launches the Tkinter GUI, blocking until the
    window is closed.
    """
    setup_logging()
    logger.info("Starting media_puller GUI")
    gui = DownloaderGUI()
    gui.run()


if __name__ == "__main__":
    main()
