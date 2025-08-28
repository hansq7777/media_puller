# media_puller

Toolkit for pulling media from a user URL using
[gallery-dl](https://github.com/mikf/gallery-dl).

## Installation

Use the provided batch script or run the command manually:

```batch
install.bat
```

or

```bash
pip install -r requirements.txt
```

## Cookie configuration

1. Export your browser cookies (Chrome format works well).
2. Launch the application and choose the cookies file via the "选择Cookies"
   button.

## Running the GUI

```batch
run.bat
```

or

```bash
python -m src.app
```

## Testing

```bash
pytest
```

## FAQ

* **gallery-dl not found** – ensure `gallery-dl` is installed and available on
  the `PATH`.
* **Downloads fail** – check the log output and verify your network
  connectivity.
* **Authentication issues** – confirm the cookies file path is correct and the
  cookies have not expired.
* **WinError 32** – indicates a file is locked by another process. Close file
  viewers, disable antivirus scans, and remove stale `.part` files before
  retrying.

## Performance tuning

* Adjust the rate limit or sleep parameter to balance speed and server load.
* Disable the download archive if re-downloading content is acceptable.
* Enable deduplication to automatically remove files with identical content.

## Updating

```batch
update.bat
```

or

```bash
git pull
```
