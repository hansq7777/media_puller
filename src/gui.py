"""Tkinter based graphical interface for media_puller."""
from __future__ import annotations

import logging
import os
import re
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from . import duplicates, gallery_dl_wrapper

logger = logging.getLogger(__name__)


class DownloaderGUI:
    """Main application window for downloading media.

    This class sets up a Tkinter interface allowing users to configure and
    launch ``gallery-dl`` downloads.
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Media Puller")
        self._build_widgets()
        self.cookies_path: Optional[str] = None
        self.directory_path: Optional[str] = None

    def _build_widgets(self) -> None:
        """Create and arrange widgets in the main window."""
        # URL entry
        tk.Label(self.root, text="用户地址").grid(row=0, column=0, sticky="e")
        self.url_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.url_var, width=50).grid(row=0, column=1, padx=5, pady=5)

        # Cookies selection
        tk.Button(self.root, text="选择Cookies", command=self.select_cookies).grid(row=1, column=0, pady=5)
        self.cookies_label = tk.Label(self.root, text="未选择")
        self.cookies_label.grid(row=1, column=1, sticky="w")

        # Directory selection
        tk.Button(self.root, text="选择下载目录", command=self.select_directory).grid(row=2, column=0, pady=5)
        self.directory_label = tk.Label(self.root, text="未选择")
        self.directory_label.grid(row=2, column=1, sticky="w")

        # Download archive checkbox
        self.archive_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="记录已下载", variable=self.archive_var).grid(row=3, column=0, sticky="w")

        # Rate limit
        tk.Label(self.root, text="速率限制").grid(row=4, column=0, sticky="e")
        self.rate_var = tk.StringVar(value="1M")
        self.rate_combo = ttk.Combobox(self.root, textvariable=self.rate_var, values=["500K", "1M", "2M", "5M"])
        self.rate_combo.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Dedupe checkbox
        self.dedupe_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="下载后查重", variable=self.dedupe_var).grid(row=5, column=0, sticky="w")

        # Start button
        tk.Button(self.root, text="开始下载", command=self.start_download).grid(row=6, column=0, columnspan=2, pady=10)

    def run(self) -> None:
        """Start the Tkinter main loop."""
        self.root.mainloop()

    def select_cookies(self) -> None:
        """Prompt user to select a cookies file."""
        path = filedialog.askopenfilename(title="选择Chrome导出的Cookies")
        if path:
            self.cookies_path = path
            self.cookies_label.config(text=path)
            logger.info("Selected cookies file: %s", path)

    def select_directory(self) -> None:
        """Prompt user to select a download directory."""
        path = filedialog.askdirectory(title="选择下载目录")
        if path:
            self.directory_path = path
            self.directory_label.config(text=path)
            logger.info("Selected download directory: %s", path)

    def start_download(self) -> None:
        """Collect parameters and start the download in a separate thread."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("错误", "请填写用户地址")
            return
        if not url.endswith("/media"):
            url += "/media"

        rate_limit = self.rate_var.get().strip() or None
        if rate_limit and not re.match(r"^\d+(\.\d+)?([KMGkmg])?$", rate_limit):
            messagebox.showerror("错误", "速率限制格式错误")
            return

        extra_args = []
        download_archive = None
        if self.directory_path:
            extra_args.extend(["--directory", self.directory_path])
        if self.archive_var.get():
            if not self.directory_path:
                messagebox.showerror("错误", "启用记录需选择下载目录")
                return
            download_archive = os.path.join(self.directory_path, "downloaded.txt")

        thread = threading.Thread(
            target=self._run_download,
            args=(url, self.cookies_path, download_archive, rate_limit, extra_args or None),
        )
        thread.start()

    def _run_download(
        self,
        url: str,
        cookies: Optional[str],
        download_archive: Optional[str],
        rate_limit: Optional[str],
        extra_args: Optional[list[str]],
    ) -> None:
        """Execute gallery-dl and handle completion or failure."""
        try:
            gallery_dl_wrapper.execute(
                url,
                cookies=cookies,
                download_archive=download_archive,
                rate_limit=rate_limit,
                extra_args=extra_args,
            )
            if self.dedupe_var.get():
                self._dedupe()
            messagebox.showinfo("完成", "下载结束")
        except gallery_dl_wrapper.GalleryDLError as exc:
            messagebox.showerror("下载失败", str(exc))

    def _dedupe(self) -> None:
        """Remove duplicate files in the selected directory.

        This function is invoked after a successful download when the user
        enables the "下载后查重" option. Errors are shown to the user and logged.
        """
        if not self.directory_path:
            logger.warning("Deduplication requested but no directory selected")
            return
        try:
            removed = duplicates.remove_duplicates(self.directory_path)
            logger.info("Deduplication removed %d files", len(removed))
        except (ValueError, OSError) as exc:
            logger.error("Deduplication failed: %s", exc)
            messagebox.showerror("查重失败", str(exc))
