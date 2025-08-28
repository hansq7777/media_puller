"""Application entry point for media_puller."""
from __future__ import annotations

import logging

from .gui import DownloaderGUI

logging.basicConfig(level=logging.INFO)


def main() -> None:
    """Start the GUI application."""
    gui = DownloaderGUI()
    gui.run()


if __name__ == "__main__":
    main()
